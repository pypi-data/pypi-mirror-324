import httpx
from typing import Optional, Any, AsyncIterator, Union, Iterator, List, Dict
import jwt
from langgraph_sdk import get_client, get_sync_client
from .exceptions import AuthenticationError, GraphError, APIError, APIKeyError, InputError, GraphNotFoundError, GraphNotPurchasedError
from .config import Config
from enum import Enum
import time
import asyncio
import os
import logging

logging.getLogger("httpx").setLevel(logging.WARNING)

class StreamMode(str, Enum):
    """Enum defining available stream modes for run execution.

    Attributes:
        MESSAGES: Stream message updates from the graph
        VALUES: Stream value updates from graph nodes
        UPDATES: Stream general state updates
        CUSTOM: Stream custom-defined updates
    """
    MESSAGES = "messages"
    VALUES = "values"
    UPDATES = "updates"
    CUSTOM = "custom"

class MultitaskStrategy(str, Enum):
    """Enum defining strategies for handling concurrent tasks on a thread.

    Attributes:
        REJECT: Reject new tasks if thread is busy
        ROLLBACK: Roll back current task and start new one
        INTERRUPT: Pause current task for human interaction
        ENQUEUE: Queue new tasks to run after current one
    """
    REJECT = "reject"
    ROLLBACK = "rollback"
    INTERRUPT = "interrupt"
    ENQUEUE = "enqueue"

class ThreadStatus(str, Enum):
    """Enum representing possible thread states.

    Attributes:
        IDLE: Thread is available for new tasks
        BUSY: Thread is currently processing a task
        INTERRUPTED: Thread is paused waiting for human input
    """
    IDLE = "idle"
    BUSY = "busy"
    INTERRUPTED = "interrupted"

class AsyncStreamWrapper:
    """Wrapper to convert a synchronous generator to an async iterator."""

    def __init__(self, async_generator, run_tracker=None):
        self.async_generator = async_generator
        self.run_tracker = run_tracker
        self.run_id = None

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            chunk = await self.async_generator.__anext__()

            # Track run_id if needed
            if self.run_tracker and not self.run_id:
                # Handle both dict and StreamPart objects
                event = getattr(chunk, 'event', None) or (chunk.get('event') if isinstance(chunk, dict) else None)
                data = getattr(chunk, 'data', None) or (chunk.get('data') if isinstance(chunk, dict) else None)

                if event == "metadata" and isinstance(data, dict) and "run_id" in data:
                    self.run_id = data["run_id"]
                    await self.run_tracker(self.run_id)

            return chunk

        except StopAsyncIteration:
            raise
        except Exception as e:
            raise

class LmsystemsClient:
    """Asynchronous client for the Lmsystems API that wraps LangGraph functionality.

    This client provides high-level access to graph execution with proper error handling,
    state management, and streaming support. It handles authentication and provides
    a simpler interface compared to direct LangGraph usage.

    Example:
        ```python
        # Initialize client
        client = await LmsystemsClient.create(
            graph_name="github-agentz-6",
            api_key="your-api-key"
        )

        # Create thread and stream run
        thread = await client.create_thread()
        async for chunk in client.stream_run(
            thread=thread,
            input={
                "messages": [{"role": "user", "content": "What's this repo about?"}],
                "repo_url": "https://github.com/user/repo",
                "chat_mode": "ask"
            },
            stream_mode=["messages"]
        ):
            print(chunk)
        ```

    Attributes:
        graph_name: Name of the purchased graph
        api_key: API key for authentication
        base_url: Base URL for the API
        client: Underlying LangGraph client instance
        default_assistant_id: Default assistant ID from graph info
    """

    def __init__(
        self,
        graph_name: str,
        api_key: str,
        base_url: str = Config.DEFAULT_BASE_URL,
    ) -> None:
        """Initialize the Lmsystems client."""
        # Disable all tracing before any other initialization
        os.environ["LANGSMITH_TRACING_V2"] = "false"
        os.environ["LANGCHAIN_TRACING"] = "false"
        os.environ["LANGCHAIN_ENABLE_TRACING"] = "false"
        os.environ["LANGSMITH_TRACING_ENABLED"] = "false"

        self.graph_name = graph_name
        self.api_key = api_key

        # Fix base URL handling
        if not base_url:
            base_url = "https://api.lmsystems.ai"
        if not base_url.startswith(("http://", "https://")):
            base_url = f"https://{base_url}"
        # Remove trailing slash only
        self.base_url = base_url.rstrip('/')

        self.client = None
        self.default_assistant_id = None
        self.configurables = None  # Added to store configurables
        self.default_environment_variables = {}  # Store default env vars

    @classmethod
    async def create(
        cls,
        graph_name: str,
        api_key: str,
        base_url: str = Config.DEFAULT_BASE_URL,
    ) -> "LmsystemsClient":
        """Async factory method to create and initialize the client."""
        client = cls(graph_name, api_key, base_url)
        await client.setup()
        return client

    async def setup(self) -> None:
        """Initialize the client asynchronously."""
        try:
            # Get graph info and store it
            self.graph_info = await self._get_graph_info()
            if not self.graph_info:
                raise APIError("Failed to get graph info from server")

            # Extract assistant_id
            self.default_assistant_id = self.graph_info.get('assistant_id')

            # Extract configurables - handle the nested structure from server response
            configurables_data = self.graph_info.get('configurables', {})
            if isinstance(configurables_data, dict):
                self.configurables = configurables_data.get('configurable', {})
            else:
                self.configurables = {}

            # Store default environment variables
            self.default_environment_variables = self.graph_info.get('environment_variables', {})

            # Set environment variables
            os.environ["LANGSMITH_TRACING_V2"] = "false"
            os.environ["LANGSMITH_TRACING"] = "false"
            os.environ["LANGSMITH_ENABLE_TRACING"] = "false"
            os.environ["LANGSMITH_TRACING_ENABLED"] = "false"

            # Initialize client
            if not self.graph_info.get('graph_url') or not self.graph_info.get('lgraph_api_key'):
                raise APIError("Missing required graph connection details")

            self.client = get_client(
                url=self.graph_info['graph_url'],
                api_key=self.graph_info['lgraph_api_key'],
                headers={
                    "x-langsmith-disable-tracing": "true",
                    "x-langsmith-tracing-v2": "false"
                }
            )
        except Exception as e:
            raise APIError(f"Failed to initialize client: {str(e)}")

    async def _get_graph_info(self) -> dict:
        """Authenticate and retrieve graph connection details."""
        try:
            async with httpx.AsyncClient() as client:
                # Ensure clean URL path joining
                url = f"{self.base_url}/api/get_graph_info"
                response = await client.post(
                    url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={"graph_name": self.graph_name}
                )

                if response.status_code != 200:
                    error_data = response.json()
                    error_type = error_data.get("detail", {}).get("error", "unknown_error")
                    error_message = error_data.get("detail", {}).get("message", "Unknown error occurred")

                    if error_type == "missing_api_key":
                        raise APIKeyError("API key is required")
                    elif error_type == "invalid_api_key":
                        raise APIKeyError("Invalid API key provided")
                    elif error_type == "missing_graph_name":
                        raise InputError("Graph name is required")
                    elif error_type == "invalid_graph_name":
                        raise InputError(error_message)
                    elif error_type == "graph_not_found":
                        raise GraphNotFoundError(self.graph_name)
                    elif error_type == "graph_not_purchased":
                        raise GraphNotPurchasedError(self.graph_name)
                    else:
                        raise APIError(f"Backend API error: {error_message}")

                return response.json()

        except httpx.RequestError as e:
            raise APIError(f"Failed to communicate with server: {str(e)}")
        except Exception as e:
            if isinstance(e, LmsystemsError):
                raise
            raise APIError(f"Unexpected error: {str(e)}")

    def _extract_api_key(self, access_token: str) -> str:
        """Extract LangGraph API key from JWT token."""
        try:
            decoded = jwt.decode(access_token, options={"verify_signature": False})
            lgraph_api_key = decoded.get("lgraph_api_key")
            if not lgraph_api_key:
                raise AuthenticationError("LangGraph API key not found in token")
            return lgraph_api_key
        except jwt.InvalidTokenError as e:
            raise AuthenticationError(f"Invalid access token: {str(e)}")

    # Helper method to handle thread ID format
    def _get_thread_id(self, thread: dict) -> str:
        """Extract thread ID from response, handling both formats."""
        if "thread_id" in thread:
            return thread["thread_id"]
        elif "id" in thread:
            return thread["id"]
        raise APIError("Invalid thread response format")

    # Delegate methods with improved error handling
    async def create_thread(self, **kwargs) -> dict:
        """Create a new thread with error handling."""
        try:
            return await self.client.threads.create(**kwargs)
        except Exception as e:
            raise APIError(f"Failed to create thread: {str(e)}")

    def _merge_environment_variables(self, user_environment: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """Merge default and user-provided environment variables.

        Args:
            user_environment: Optional dictionary of environment variables to override defaults

        Returns:
            Dict[str, str]: Merged environment variables with user overrides

        Raises:
            APIError: If environment variables are not in the correct format
        """
        try:
            # Validate default environment variables
            if not isinstance(self.default_environment_variables, dict):
                merged = {}
            else:
                merged = {
                    str(k): str(v)
                    for k, v in self.default_environment_variables.items()
                    if k is not None and v is not None
                }

            # Validate and merge user environment variables
            if user_environment:
                if not isinstance(user_environment, dict):
                    raise APIError("Environment variables must be a dictionary")

                # Convert all keys and values to strings
                user_env = {
                    str(k): str(v)
                    for k, v in user_environment.items()
                    if k is not None and v is not None
                }
                merged.update(user_env)

            return merged
        except Exception as e:
            if isinstance(e, APIError):
                raise
            raise APIError(f"Failed to process environment variables: {str(e)}")

    async def create_run(
        self,
        thread: dict,
        *,
        input: dict,
        environment: Optional[Dict[str, str]] = None,
        config: Optional[Dict[str, Any]] = None,
        assistant_id: Optional[str] = None,
        multitask_strategy: Optional[str] = MultitaskStrategy.REJECT,
        wait_for_idle: bool = True,
        timeout: int = 30,
    ) -> dict:
        """Create a run with environment variable support."""
        try:
            thread_id = thread.get("thread_id") or thread.get("id")
            if not thread_id:
                raise APIError("Invalid thread format")

            # Check thread status if we're not using REJECT strategy
            if multitask_strategy != MultitaskStrategy.REJECT:
                status = await self.get_thread_status(thread)
                if status == ThreadStatus.BUSY:
                    if wait_for_idle:
                        if not await self.wait_for_thread(thread, timeout):
                            raise APIError(f"Thread still busy after {timeout} seconds")
                    else:
                        raise APIError("Thread is busy. Set wait_for_idle=True to wait")

            # Use provided assistant_id or fall back to default
            assistant_id = assistant_id or self.default_assistant_id
            if not assistant_id:
                raise APIError("No assistant_id provided and no default available")

            # Use the user-provided input directly.
            final_input = input.copy() if isinstance(input, dict) else input

            run = await self.client.runs.create(
                thread_id=thread_id,
                assistant_id=assistant_id,
                input=final_input,
                multitask_strategy=multitask_strategy,
                **({"config": config} if config else {})
            )

            # Tracks run directly after creation
            if run.get("run_id"):
                await self._track_run(run["run_id"])

            return run

        except Exception as e:
            raise APIError(f"Failed to create run: {str(e)}")

    async def _track_run(self, run_id: str) -> None:
        """Track a new run with the backend."""
        try:
            url = f"{self.base_url}/api/track_run"

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "graph_name": self.graph_name,
                        "run_id": run_id
                    }
                )
                if response.status_code != 200:
                    print(f"Warning: Failed to track run usage: {response.text}")
        except Exception as e:
            print(f"Warning: Failed to track run: {str(e)}")

    def _inject_configurables(self, input_dict: dict) -> dict:
        """Helper to inject configurables into input state.

        Only injects configurable values if their lowercase key doesn't already exist in input.

        Args:
            input_dict: Original input dictionary

        Returns:
            dict: Input dictionary enriched with non-duplicate configurable values
        """
        try:
            if not isinstance(input_dict, dict):
                return input_dict

            # Create a copy of input to avoid mutations
            enriched_input = dict(input_dict)

            # Create set of lowercase input keys for efficient lookup
            existing_keys = {key.lower() for key in input_dict.keys()}

            if self.configurables:
                for key, config in self.configurables.items():
                    if isinstance(config, dict) and 'value' in config:
                        # Convert key from UPPERCASE to lowercase for state variables
                        state_key = key.lower()
                        # Only inject if key doesn't already exist in input
                        if state_key not in existing_keys:
                            enriched_input[state_key] = config['value']

            return enriched_input
        except Exception as e:
            raise APIError(f"Failed to prepare input: {str(e)}")

    async def stream_run(
        self,
        thread: dict,
        input: dict,
        *,
        assistant_id: Optional[str] = None,
        environment: Optional[Dict[str, str]] = None,
        config: Optional[Dict[str, Any]] = None,
        stream_mode: Union[str, List[str]] = ["messages"],
        multitask_strategy: Optional[str] = MultitaskStrategy.REJECT,
        wait_for_idle: bool = True,
        timeout: int = 30,
        interrupt_before: Optional[List[str]] = None,
    ) -> AsyncIterator[dict]:
        """Stream a run with proper thread state handling.

        This is the recommended way to execute graph runs as it handles thread state
        management and provides real-time streaming of results.

        Example:
            ```python
            async for chunk in client.stream_run(
                thread=thread,
                input={
                    "messages": [{"role": "user", "content": "Analyze this repo"}],
                    "repo_url": "https://github.com/user/repo",
                    "chat_mode": "ask"
                },
                stream_mode=["messages", "updates"],
                multitask_strategy=MultitaskStrategy.INTERRUPT
            ):
                print(chunk)
            ```

        Args:
            thread: Thread dict containing thread_id
            input: Input data for the run
            assistant_id: Optional assistant ID (defaults to self.default_assistant_id)
            environment: Optional environment variables for the run
            stream_mode: What to stream (default: ["messages"])
            multitask_strategy: How to handle concurrent tasks
            wait_for_idle: Whether to wait for thread to become idle if busy
            timeout: Maximum time to wait for thread to become idle
            interrupt_before: Optional list of node names to interrupt before

        Returns:
            AsyncIterator yielding streamed responses

        Raises:
            APIError: If thread is busy and wait_for_idle is False, or other API errors
        """
        try:
            thread_id = thread.get("thread_id") or thread.get("id")
            if not thread_id:
                raise APIError("Invalid thread format")

            # Check thread status if we're not using REJECT strategy
            if multitask_strategy != MultitaskStrategy.REJECT:
                status = await self.get_thread_status(thread)
                if status == ThreadStatus.BUSY:
                    if wait_for_idle:
                        if not await self.wait_for_thread(thread, timeout):
                            raise APIError(f"Thread still busy after {timeout} seconds")
                    else:
                        raise APIError("Thread is busy. Set wait_for_idle=True to wait")

            # Use provided assistant_id or fall back to default
            assistant_id = assistant_id or self.default_assistant_id
            if not assistant_id:
                raise APIError("No assistant_id available")

            # Always ensure stream_mode is a list
            if isinstance(stream_mode, str):
                stream_mode = [stream_mode]

            # Use the user-provided input directly.
            final_input = input.copy() if isinstance(input, dict) else input

            async_generator = self.client.runs.stream(
                thread_id,
                assistant_id,
                input=final_input,
                stream_mode=stream_mode,
                multitask_strategy=multitask_strategy,
                interrupt_before=interrupt_before,
                **({"config": config} if config else {})
            )

            async_iterator = AsyncStreamWrapper(async_generator, self._track_run)
            async for chunk in async_iterator:
                yield chunk

        except Exception as e:
            raise APIError(f"Failed to stream run: {str(e)}")

    async def stream_run_events(
        self,
        thread: dict,
        run: dict,
        *,
        version: str = "v1"
    ) -> AsyncIterator[dict]:
        """Stream individual events from a run.

        Args:
            thread: Thread object containing thread_id
            run: Run object containing run_id
            version: Event format version ("v1" or "v2")

        Returns:
            AsyncIterator yielding event objects
        """
        try:
            thread_id = self._get_thread_id(thread)
            run_id = run.get("run_id") or run.get("id")

            if not run_id:
                raise APIError("Invalid run response format")

            async for event in self.client.runs.stream_events(
                thread_id=thread_id,
                run_id=run_id,
                version=version
            ):
                yield event

        except Exception as e:
            raise APIError(f"Failed to stream run events: {str(e)}")

    @property
    def assistants(self):
        """Access the assistants API."""
        return self.client.assistants

    @property
    def threads(self):
        """Access the threads API."""
        return self.client.threads

    @property
    def runs(self):
        """Access the runs API."""
        return self.client.runs

    @property
    def crons(self):
        """Access the crons API."""
        return self.client.crons

    @property
    def store(self):
        """Access the store API."""
        return self.client.store

    async def get_thread_status(self, thread: dict) -> str:
        """Get the current status of a thread."""
        thread_id = thread.get("thread_id") or thread.get("id")
        if not thread_id:
            raise APIError("Invalid thread format")

        thread_info = await self.threads.get(thread_id)
        return thread_info.get("status", ThreadStatus.IDLE)

    async def wait_for_thread(self, thread: dict, timeout: int = 30) -> bool:
        """Wait for thread to become idle, with timeout."""
        thread_id = thread.get("thread_id") or thread.get("id")
        start_time = time.time()

        while time.time() - start_time < timeout:
            status = await self.get_thread_status(thread)
            if status == ThreadStatus.IDLE:
                return True
            await asyncio.sleep(1)
        return False

    def get_thread_state(self, thread: dict) -> dict:
        """Get the current state of a thread."""
        thread_id = thread.get("thread_id") or thread.get("id")
        if not thread_id:
            raise APIError("Invalid thread format")
        return self.client.threads.get_state(thread_id)

    def update_thread_state(self, thread: dict, state_update: dict, *, as_node: str = None) -> dict:
        """Update the state of a thread."""
        thread_id = thread.get("thread_id") or thread.get("id")
        if not thread_id:
            raise APIError("Invalid thread format")

        # Pass state_update directly as first argument after thread_id
        if as_node:
            return self.client.threads.update_state(thread_id, state_update, as_node=as_node)
        return self.client.threads.update_state(thread_id, state_update)


class SyncLmsystemsClient:
    """Synchronous client for the Lmsystems API that wraps LangGraph functionality.

    This provides the same interface as LmsystemsClient but in a synchronous form,
    suitable for scripts and applications that don't use async/await.

    Example:
        ```python
        # Initialize client
        client = SyncLmsystemsClient(
            graph_name="github-agentz-6",
            api_key="your-api-key"
        )

        # Create thread and stream run
        thread = client.threads.create()
        for chunk in client.stream_run(
            thread=thread,
            input={
                "messages": [{"role": "user", "content": "What's this repo about?"}],
                "repo_url": "https://github.com/user/repo",
                "chat_mode": "ask"
            },
            stream_mode=["messages"]
        ):
            print(chunk)
        ```

    Example (Resuming Interrupted Graph):
        ```python
        # Resume from interrupted state
        thread = {"thread_id": "existing-thread-id"}

        # Update state at specific node
        client.update_thread_state(
            thread=thread,
            state_update={
                "messages": [{"role": "user", "content": "continue"}],
                "accepted": True
            },
            as_node="human_interaction"
        )

        # Resume with checkpoint
        for chunk in client.stream_run(
            thread=thread,
            input=None,
            checkpoint_id=checkpoint_id
        ):
            print(chunk)
        ```

    Attributes:
        graph_name: Name of the purchased graph
        api_key: API key for authentication
        base_url: Base URL for the API
        client: Underlying LangGraph sync client instance
        default_assistant_id: Default assistant ID from graph info
    """


    def __init__(
        self,
        graph_name: str,
        api_key: str,
        base_url: str = Config.DEFAULT_BASE_URL,
    ) -> None:
        """Initialize the synchronous client."""
        self.graph_name = graph_name
        self.api_key = api_key
        self.base_url = base_url

        # Initialize these in setup
        self.client = None
        self.default_assistant_id = None
        self.graph_info = None
        self.default_environment_variables = {}

        # Call setup immediately for sync client
        self.setup()

    def setup(self) -> None:
        """Initialize the client synchronously."""
        try:
            # Get graph info and store it
            self.graph_info = self._get_graph_info()
            if not self.graph_info:
                raise APIError("Failed to get graph info from server")

            # Extract assistant_id
            self.default_assistant_id = self.graph_info.get('assistant_id')

            # Extract configurables - handle the nested structure from server response
            configurables_data = self.graph_info.get('configurables', {})
            if isinstance(configurables_data, dict):
                self.configurables = configurables_data.get('configurable', {})
            else:
                self.configurables = {}

            # Store default environment variables
            self.default_environment_variables = self.graph_info.get('environment_variables', {})

            # Set environment variables
            os.environ["LANGSMITH_TRACING_V2"] = "false"
            os.environ["LANGSMITH_TRACING"] = "false"
            os.environ["LANGSMITH_ENABLE_TRACING"] = "false"
            os.environ["LANGSMITH_TRACING_ENABLED"] = "false"

            # Initialize client
            if not self.graph_info.get('graph_url') or not self.graph_info.get('lgraph_api_key'):
                raise APIError("Missing required graph connection details")

            self.client = get_sync_client(
                url=self.graph_info['graph_url'],
                api_key=self.graph_info['lgraph_api_key'],
                headers={
                    "x-langsmith-disable-tracing": "true",
                    "x-langsmith-tracing-v2": "false"
                }
            )
        except Exception as e:
            raise APIError(f"Failed to initialize client: {str(e)}")

    def _get_graph_info(self) -> dict:
        """Synchronous version of getting graph info."""
        try:
            with httpx.Client() as client:
                response = client.post(
                    f"{self.base_url}/api/get_graph_info",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={"graph_name": self.graph_name}
                )

                if response.status_code == 401:
                    raise AuthenticationError("Invalid API key")
                elif response.status_code == 403:
                    raise GraphError(f"Graph '{self.graph_name}' has not been purchased")
                elif response.status_code == 404:
                    raise GraphError(f"Graph '{self.graph_name}' not found")
                elif response.status_code != 200:
                    raise APIError(f"Backend API error: {response.text}")

                data = response.json()
                if not isinstance(data, dict):
                    raise APIError("Invalid response format from server")
                return data

        except httpx.RequestError as e:
            raise APIError(f"Failed to connect to backend: {str(e)}")
        except Exception as e:
            if isinstance(e, (AuthenticationError, GraphError, APIError)):
                raise
            raise APIError(f"Unexpected error getting graph info: {str(e)}")

    def _extract_api_key(self, access_token: str) -> str:
        """Extract LangGraph API key from JWT token."""
        try:
            decoded = jwt.decode(access_token, options={"verify_signature": False})
            if 'lgraph_api_key' not in decoded:
                raise AuthenticationError("Invalid token format")
            return decoded['lgraph_api_key']
        except jwt.InvalidTokenError as e:
            raise AuthenticationError(f"Invalid access token: {str(e)}")

    @property
    def assistants(self):
        """Access the assistants API."""
        return self.client.assistants

    @property
    def threads(self):
        """Access the threads API."""
        return self.client.threads

    @property
    def runs(self):
        """Access the runs API."""
        return self.client.runs

    @property
    def crons(self):
        """Access the crons API."""
        return self.client.crons

    @property
    def store(self):
        """Access the store API."""
        return self.client.store

    def _merge_environment_variables(self, user_environment: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """Merge default and user-provided environment variables.

        Args:
            user_environment: Optional dictionary of environment variables to override defaults

        Returns:
            Dict[str, str]: Merged environment variables with user overrides

        Raises:
            APIError: If environment variables are not in the correct format
        """
        try:
            # Validate default environment variables
            if not isinstance(self.default_environment_variables, dict):
                merged = {}
            else:
                merged = {
                    str(k): str(v)
                    for k, v in self.default_environment_variables.items()
                    if k is not None and v is not None
                }

            # Validate and merge user environment variables
            if user_environment:
                if not isinstance(user_environment, dict):
                    raise APIError("Environment variables must be a dictionary")

                # Convert all keys and values to strings
                user_env = {
                    str(k): str(v)
                    for k, v in user_environment.items()
                    if k is not None and v is not None
                }
                merged.update(user_env)

            return merged
        except Exception as e:
            if isinstance(e, APIError):
                raise
            raise APIError(f"Failed to process environment variables: {str(e)}")

    def _inject_configurables(self, input_dict: dict) -> dict:
        """Helper to inject configurables into input state.

        Only injects configurable values if their lowercase key doesn't already exist in input.

        Args:
            input_dict: Original input dictionary

        Returns:
            dict: Input dictionary enriched with non-duplicate configurable values
        """
        try:
            if not isinstance(input_dict, dict):
                return input_dict

            # Create a copy of input to avoid mutations
            enriched_input = dict(input_dict)

            # Create set of lowercase input keys for efficient lookup
            existing_keys = {key.lower() for key in input_dict.keys()}

            if self.configurables:
                for key, config in self.configurables.items():
                    if isinstance(config, dict) and 'value' in config:
                        # Convert key from UPPERCASE to lowercase for state variables
                        state_key = key.lower()
                        # Only inject if key doesn't already exist in input
                        if state_key not in existing_keys:
                            enriched_input[state_key] = config['value']

            return enriched_input
        except Exception as e:
            raise APIError(f"Failed to prepare input: {str(e)}")

    def create_run(
        self,
        thread: dict,
        *,
        input: dict,
        assistant_id: Optional[str] = None,
        multitask_strategy: Optional[str] = MultitaskStrategy.REJECT,
        wait_for_idle: bool = True,
        timeout: int = 30,
    ) -> dict:
        """Create a run with proper thread state handling."""
        try:
            thread_id = thread.get("thread_id") or thread.get("id")
            if not thread_id:
                raise APIError("Invalid thread format")

            # Check thread status if we're not using REJECT strategy
            if multitask_strategy != MultitaskStrategy.REJECT:
                status = self.get_thread_status(thread)
                if status == ThreadStatus.BUSY:
                    if wait_for_idle:
                        if not self.wait_for_thread(thread, timeout):
                            raise APIError(f"Thread still busy after {timeout} seconds")
                    else:
                        raise APIError("Thread is busy. Set wait_for_idle=True to wait")

            # Use provided assistant_id or fall back to default
            assistant_id = assistant_id or self.default_assistant_id
            if not assistant_id:
                raise APIError("No assistant_id provided and no default available")

            run = self.client.runs.create(
                thread_id=thread_id,
                assistant_id=assistant_id,
                input=input,
                multitask_strategy=multitask_strategy
            )

            # Tracks run directly after creation
            if run.get("run_id"):
                self._track_run(run["run_id"])

            return run

        except Exception as e:
            raise APIError(f"Failed to create run: {str(e)}")

    def _track_run(self, run_id: str) -> None:
        """Track a new run with the backend."""
        try:
            url = f"{self.base_url}/api/track_run"
            with httpx.Client() as client:
                response = client.post(
                    url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "graph_name": self.graph_name,
                        "run_id": run_id
                    }
                )
        except Exception as e:
            print(f"Warning: Failed to track run usage: {str(e)}")
            print(f"Current base_url: {self.base_url}")  # Debug log

    def stream_run(
        self,
        thread: dict,
        input: dict,
        *,
        assistant_id: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
        stream_mode: Union[str, List[str]] = ["messages"],
        multitask_strategy: Optional[str] = MultitaskStrategy.REJECT,
    ) -> Iterator[dict]:
        try:
            thread_id = thread.get("thread_id") or thread.get("id")
            if not thread_id:
                raise APIError("Invalid thread format")

            assistant_id = assistant_id or self.default_assistant_id
            if not assistant_id:
                raise APIError("No assistant_id available")

            if isinstance(stream_mode, str):
                stream_mode = [stream_mode]

            # Use the user-provided input directly.
            final_input = input.copy() if isinstance(input, dict) else input

            # Track run_id for usage tracking
            run_id = None
            for chunk in self.client.runs.stream(
                thread_id,
                assistant_id,
                input=final_input,
                stream_mode=stream_mode,
                multitask_strategy=multitask_strategy,
                **({"config": config} if config else {})
            ):
                if not run_id:
                    event = getattr(chunk, 'event', None) or (chunk.get('event') if isinstance(chunk, dict) else None)
                    data = getattr(chunk, 'data', None) or (chunk.get('data') if isinstance(chunk, dict) else None)

                    if event == "metadata" and isinstance(data, dict) and "run_id" in data:
                        run_id = data["run_id"]
                        self._track_run(run_id)
                yield chunk

        except Exception as e:
            raise APIError(f"Failed to stream run: {str(e)}")

    def stream_run_events(
        self,
        thread: dict,
        run: dict,
        *,
        version: str = "v1"
    ) -> Iterator[dict]:
        """Synchronous version of stream_run_events."""
        try:
            thread_id = thread.get("thread_id") or thread.get("id")
            run_id = run.get("run_id") or run.get("id")

            if not thread_id or not run_id:
                raise APIError("Invalid thread or run format")

            # Note the positional args here too
            for event in self.client.runs.stream_events(
                thread_id,  # Changed: removed keyword argument
                run_id,    # Changed: removed keyword argument
                version=version
            ):
                yield event

        except Exception as e:
            raise APIError(f"Failed to stream run events: {str(e)}")

    def get_thread_status(self, thread: dict) -> str:
        """Get the current status of a thread."""
        thread_id = thread.get("thread_id") or thread.get("id")
        if not thread_id:
            raise APIError("Invalid thread format")

        thread_info = self.threads.get(thread_id)
        return thread_info.get("status", ThreadStatus.IDLE)

    def wait_for_thread(self, thread: dict, timeout: int = 30) -> bool:
        """Wait for thread to become idle, with timeout."""
        thread_id = thread.get("thread_id") or thread.get("id")
        start_time = time.time()

        while time.time() - start_time < timeout:
            status = self.get_thread_status(thread)
            if status == ThreadStatus.IDLE:
                return True
            time.sleep(1)
        return False

    def get_thread_state(self, thread: dict) -> dict:
        """Get the current state of a thread."""
        thread_id = thread.get("thread_id") or thread.get("id")
        if not thread_id:
            raise APIError("Invalid thread format")
        return self.client.threads.get_state(thread_id)

    def update_thread_state(self, thread: dict, state_update: dict, *, as_node: str = None) -> dict:
        """Update the state of a thread."""
        thread_id = thread.get("thread_id") or thread.get("id")
        if not thread_id:
            raise APIError("Invalid thread format")

        # Pass state_update directly as first argument after thread_id
        if as_node:
            return self.client.threads.update_state(thread_id, state_update, as_node=as_node)
        return self.client.threads.update_state(thread_id, state_update)
