import jwt
from typing import Any, Optional, Union, Iterator, AsyncIterator, Sequence
from langgraph.pregel.remote import RemoteGraph, RemoteException
from langchain_core.runnables import RunnableConfig
from langgraph.pregel.protocol import PregelProtocol
import requests
from .exceptions import (
    LmsystemsError,
    AuthenticationError,
    GraphError,
    InputError,
    APIError
)
import os
from lmsystems.config import Config
from langgraph.errors import GraphInterrupt
from langgraph_sdk.schema import StreamPart
from langgraph.pregel.types import All
import logging
import httpx
import orjson
import uuid


logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

class PurchasedGraph(PregelProtocol):
    """
    A wrapper class for RemoteGraph that handles marketplace authentication and graph purchasing.

    This class provides a simplified interface for working with purchased graphs from the marketplace,
    while maintaining full compatibility with LangGraph's RemoteGraph functionality.

    Attributes:
        graph_name (str): Name of the purchased graph
        api_key (str): Marketplace API key for authentication
        config (Optional[RunnableConfig]): Configuration for the graph
        default_state_values (dict): Default values to inject into graph state
        base_url (str): Marketplace API base URL
        development_mode (bool): Whether to run in development mode
        graph_info (dict): Cached graph information from marketplace
        remote_graph (RemoteGraph): Internal RemoteGraph instance

    Example:
        ```python
        graph = PurchasedGraph(
            graph_name="my-agent",
            api_key="api_key_123",
            default_state_values={
                "system_prompt": "You are a helpful assistant"
            }
        )

        result = graph.invoke({
            "messages": [{"role": "user", "content": "Hello"}]
        })
        ```
    """

    def __init__(
        self,
        graph_name: str,
        api_key: str,
        config: Optional[RunnableConfig] = None,
        default_state_values: Optional[dict[str, Any]] = None,
        base_url: str = Config.DEFAULT_BASE_URL,
    ):
        """
        Initialize a PurchasedGraph instance.

        Args:
            graph_name: The name of the purchased graph.
            api_key: The buyer's lmsystems API key.
            config: Optional RunnableConfig for additional configuration.
            default_state_values: Optional default values for required state parameters.
            base_url: The base URL of the marketplace backend.

        Raises:
            AuthenticationError: If the API key is invalid
            GraphError: If the graph doesn't exist or hasn't been purchased
            InputError: If required configuration is invalid
            APIError: If there are backend communication issues
        """
        if not api_key:
            raise AuthenticationError("API key is required.")
        if not graph_name:
            raise InputError("Graph name is required")

        self.graph_name = graph_name
        self.api_key = api_key
        self.config = config
        self.default_state_values = default_state_values or {}
        self.base_url = base_url
        self.configurables = None  # Store configurables from server

        try:
            self.graph_info = self._get_graph_info()

            # Get API key
            lgraph_api_key = self.graph_info.get('lgraph_api_key')
            if not lgraph_api_key:
                raise GraphError("LangGraph API key not found in response")

            # Extract configurables from graph info
            configurables_data = self.graph_info.get('configurables', {})
            if isinstance(configurables_data, dict):
                self.configurables = configurables_data.get('configurable', {})
            else:
                self.configurables = {}

            # Initialize RemoteGraph without config
            self.remote_graph = RemoteGraph(
                self.graph_info['graph_name'],
                url=self.graph_info['graph_url'],
                api_key=lgraph_api_key
            )

        except Exception as e:
            raise APIError(f"Failed to initialize graph: {str(e)}")

    def _get_graph_info(self) -> dict:
        """
        Authenticate with the marketplace backend and retrieve graph details.

        This method handles the initial authentication and graph validation process.
        It verifies the API key, checks if the graph exists and has been purchased,
        and retrieves necessary configuration details.

        Returns:
            dict: Graph information including:
                - graph_name: Name of the graph
                - graph_url: URL for the graph deployment
                - lgraph_api_key: LangGraph API key for authentication
                - configurables: Default configuration values

        Raises:
            AuthenticationError: If the API key is invalid
            GraphError: If the graph doesn't exist or hasn't been purchased
            APIError: If there are backend communication issues
        """
        try:
            endpoint = f"{self.base_url}/api/get_graph_info"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            payload = {"graph_name": self.graph_name}

            response = requests.post(endpoint, json=payload, headers=headers)

            if response.status_code == 401:
                raise AuthenticationError("Invalid API key.")
            elif response.status_code == 403:
                raise GraphError(f"Graph '{self.graph_name}' has not been purchased")
            elif response.status_code == 404:
                raise GraphError(f"Graph '{self.graph_name}' not found")
            elif response.status_code != 200:
                raise APIError(f"Backend API error: {response.text}")

            return response.json()
        except requests.RequestException as e:
            raise APIError(f"Failed to communicate with backend: {str(e)}")

    def _extract_api_key(self, access_token: str) -> str:
        """Extract the LangGraph API key from the JWT token without verification."""
        try:
            decoded_token = jwt.decode(access_token, options={"verify_signature": False})
            lgraph_api_key = decoded_token.get("lgraph_api_key")
            if not lgraph_api_key:
                raise APIError("LangGraph API key not found in token payload")
            return lgraph_api_key
        except jwt.InvalidTokenError as e:
            raise APIError(f"Invalid access token: {str(e)}")
        except Exception as e:
            raise APIError(f"Failed to decode token: {str(e)}")

    def _prepare_input(self, input: Union[dict[str, Any], Any]) -> dict[str, Any]:
        try:
            if not isinstance(input, dict):
                return input

            # Simply return user input without merging config values
            return input.copy() if isinstance(input, dict) else input
        except Exception as e:
            raise APIError(f"Failed to prepare input: {str(e)}")

    def merge_configs(self, base: Optional[dict], update: Optional[dict]) -> dict:
        """Merge two config dictionaries, preserving nested 'configurable' keys."""
        result = (base or {}).copy()
        if update:
            if 'configurable' in update and 'configurable' in result:
                result['configurable'].update(update['configurable'])
            else:
                result.update(update)
        return result

    def invoke(
        self,
        input: Union[dict[str, Any], Any],
        config: Optional[RunnableConfig] = None,
        **kwargs: Any
    ) -> Any:
        try:
            # Merge constructor config with method call config
            full_config = self.merge_configs(self.config, config)

            return self.remote_graph.invoke(
                input,  # Use raw input without modification
                config=full_config,  # Pass merged config
                **kwargs
            )
        except Exception as e:
            raise APIError(f"Failed to execute graph: {str(e)}")

    def stream(
        self,
        input: Union[dict[str, Any], Any],
        config: Optional[RunnableConfig] = None,
        **kwargs: Any
    ) -> Iterator[Any]:
        """Stream with configurables injected into state."""
        try:
            # Use the config from the method parameter or default to self.config
            config = config or self.config

            # Create base iterator
            base_iterator = self.remote_graph.stream(
                self._prepare_input(input),
                config=config,
                **kwargs
            )

            # Wrap with tracking
            wrapped_iterator = PurchasedGraphStreamWrapper(
                base_iterator,
                run_tracker=self
            )

            # Return wrapped iterator
            return wrapped_iterator
        except Exception as e:
            raise APIError(f"Failed to stream from graph: {str(e)}")

    async def ainvoke(
        self,
        input: Union[dict[str, Any], Any],
        config: Optional[RunnableConfig] = None,
        **kwargs: Any
    ) -> Any:
        """Async invoke with configurables injected into state."""
        try:
            # Use the config from the method parameter or default to self.config
            config = config or self.config

            # Generate run ID
            run_id = str(uuid.uuid4())

            # Track the run before executing. Raise error if tracking fails.
            await self._track_run(run_id)

            return await self.remote_graph.ainvoke(
                self._prepare_input(input),
                config=config,
                **kwargs
            )
        except Exception as e:
            raise APIError(f"Failed to execute graph: {str(e)}")

    async def astream(
        self,
        input: Union[dict[str, Any], Any],
        config: Optional[RunnableConfig] = None,
        **kwargs: Any
    ) -> AsyncIterator[Any]:
        """Async stream with configurables injected into state."""
        try:
            # Use the config from the method parameter or default to self.config
            config = config or self.config

            # Create base iterator
            base_iterator = self.remote_graph.astream(
                self._prepare_input(input),
                config=config,
                **kwargs
            )

            # Wrap with tracking
            wrapped_iterator = PurchasedGraphStreamWrapper(
                base_iterator,
                run_tracker=self
            )

            # Return wrapped iterator
            return wrapped_iterator
        except Exception as e:
            raise APIError(f"Failed to stream from graph: {str(e)}")

    def with_config(self, config: Optional[RunnableConfig] = None, **kwargs: Any) -> Any:
        """
        Return a modified copy of the 'PurchasedGraph' or its underlying
        RemoteGraph with merged config, so advanced usage can be done
        (e.g. setting thread_id).
        """
        # Option 1: just return remote_graph.with_config(...)
        #     which effectively returns a RemoteGraph.
        # Option 2: re-initialize a new PurchasedGraph if you
        #     want to preserve the same class type.
        # For simplicity, we keep returning RemoteGraph itself:
        return self.remote_graph.with_config(config, **kwargs)

    def get_graph(self, config: Optional[RunnableConfig] = None, *, xray: Union[int, bool] = False) -> Any:
        return self.remote_graph.get_graph(config=config, xray=xray)

    async def aget_graph(self, config: Optional[RunnableConfig] = None, *, xray: Union[int, bool] = False) -> Any:
        return await self.remote_graph.aget_graph(config=config, xray=xray)

    def get_state(self, config: RunnableConfig, *, subgraphs: bool = False) -> Any:
        return self.remote_graph.get_state(config=config, subgraphs=subgraphs)

    async def aget_state(self, config: RunnableConfig, *, subgraphs: bool = False) -> Any:
        return await self.remote_graph.aget_state(config=config, subgraphs=subgraphs)

    def get_state_history(self, config: RunnableConfig, *, filter: Optional[dict[str, Any]] = None, before: Optional[RunnableConfig] = None, limit: Optional[int] = None) -> Any:
        return self.remote_graph.get_state_history(config=config, filter=filter, before=before, limit=limit)

    async def aget_state_history(self, config: RunnableConfig, *, filter: Optional[dict[str, Any]] = None, before: Optional[RunnableConfig] = None, limit: Optional[int] = None) -> Any:
        return await self.remote_graph.aget_state_history(config=config, filter=filter, before=before, limit=limit)

    def update_state(self, config: RunnableConfig, values: Optional[Union[dict[str, Any], Any]], as_node: Optional[str] = None) -> RunnableConfig:
        return self.remote_graph.update_state(config=config, values=values, as_node=as_node)

    async def aupdate_state(self, config: RunnableConfig, values: Optional[Union[dict[str, Any], Any]], as_node: Optional[str] = None) -> RunnableConfig:
        return await self.remote_graph.aupdate_state(config=config, values=values, as_node=as_node)

    async def _track_run(self, run_id: str) -> None:
        """Async version of run tracking."""
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
                    },
                    timeout=10.0
                )

                if response.status_code != 200:
                    error_msg = f"Failed to track run usage: Status {response.status_code}"
                    try:
                        error_data = response.json()
                        if isinstance(error_data, dict):
                            error_msg = f"{error_msg} - {error_data.get('detail', error_data)}"
                    except:
                        error_msg = f"{error_msg} - {response.text}"

        except Exception:
            pass  # Silently handle tracking errors

    def _track_run_sync(self, run_id: str) -> None:
        """Synchronous version of run tracking."""
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
                    },
                    timeout=10.0
                )

                if response.status_code != 200:
                    error_msg = f"Failed to track run usage: Status {response.status_code}"
                    try:
                        error_data = response.json()
                        if isinstance(error_data, dict):
                            error_msg = f"{error_msg} - {error_data.get('detail', error_data)}"
                    except:
                        error_msg = f"{error_msg} - {response.text}"

        except Exception:
            pass  # Silently handle tracking errors

    def _sanitize_config(self, config: RunnableConfig) -> RunnableConfig:
        """Sanitize config similar to RemoteGraph."""
        if not config:
            return {"configurable": {}}

        # Copy RemoteGraph's sanitization logic
        reserved_configurable_keys = frozenset([
            "callbacks",
            "checkpoint_map",
            "checkpoint_id",
            "checkpoint_ns",
        ])

        def _sanitize_obj(obj: Any) -> Any:
            if isinstance(obj, dict):
                return {k: _sanitize_obj(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [_sanitize_obj(v) for v in obj]
            else:
                try:
                    orjson.dumps(obj)
                    return obj
                except:
                    return None

        # Sanitize the config
        config = _sanitize_obj(config)

        # Filter configurable keys
        new_configurable = {
            k: v
            for k, v in config.get("configurable", {}).items()
            if k not in reserved_configurable_keys and not k.startswith("__pregel_")
        }

        return {
            "tags": config.get("tags") or [],
            "metadata": config.get("metadata") or {},
            "configurable": new_configurable,
        }

class PurchasedGraphStreamWrapper:
    """Wrapper for tracking runs in stream responses."""

    def __init__(self, stream_iterator, run_tracker=None):
        self.stream_iterator = stream_iterator
        self.run_tracker = run_tracker
        self.run_id = None

    def __iter__(self):
        return self

    async def __aiter__(self):
        return self

    def __next__(self):
        try:
            chunk = next(self.stream_iterator)
            self._handle_chunk_sync(chunk)
            return chunk
        except StopIteration:
            raise

    async def __anext__(self):
        try:
            chunk = await self.stream_iterator.__anext__()
            await self._handle_chunk(chunk)
            return chunk
        except StopAsyncIteration:
            raise

    def _handle_chunk_sync(self, chunk):
        """Handle chunk synchronously."""
        if self.run_tracker and not self.run_id:
            event = getattr(chunk, 'event', None) or (chunk.get('event') if isinstance(chunk, dict) else None)
            data = getattr(chunk, 'data', None) or (chunk.get('data') if isinstance(chunk, dict) else None)

            if event == "metadata" and isinstance(data, dict) and "run_id" in data:
                self.run_id = data["run_id"]
                # Use synchronous tracking for sync context
                if hasattr(self.run_tracker, '_track_run_sync'):
                    self.run_tracker._track_run_sync(self.run_id)
                else:
                    logger.warning("Synchronous tracking not available")

    async def _handle_chunk(self, chunk):
        """Handle chunk asynchronously."""
        if self.run_tracker and not self.run_id:
            # Handle both dict and StreamPart objects
            event = getattr(chunk, 'event', None) or (chunk.get('event') if isinstance(chunk, dict) else None)
            data = getattr(chunk, 'data', None) or (chunk.get('data') if isinstance(chunk, dict) else None)

            if event == "metadata" and isinstance(data, dict) and "run_id" in data:
                self.run_id = data["run_id"]
                await self.run_tracker(self.run_id)

