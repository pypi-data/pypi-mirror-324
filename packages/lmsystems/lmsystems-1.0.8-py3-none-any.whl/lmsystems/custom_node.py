import aiohttp
import logging
import requests
import json
import zipfile
import io
import base64
import asyncio
from typing import Dict, Any, List, Optional, AsyncIterator, TypeVar, Generic, Union
from langchain_core.runnables import RunnableLambda, RunnableConfig
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.callbacks.manager import AsyncCallbackManager
from uuid import uuid4
from pydantic import BaseModel, Field, ValidationError

logger = logging.getLogger(__name__)

# Generic type for state
StateType = TypeVar("StateType")

class BaseState(BaseModel):
    """Base class for state validation."""
    messages: List[Dict[str, str]] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    version: str = Field(default="1.0")

class StateManager(Generic[StateType]):
    """Manages state validation and transformation."""

    def __init__(self, state_class: Optional[type] = None):
        self.state_class = state_class or BaseState

    def validate_state(self, state: Dict[str, Any]) -> StateType:
        """Validate and convert state to proper format."""
        try:
            # If state is already a Pydantic model of the correct type
            if isinstance(state, self.state_class):
                return state

            # If it's a dict, create new instance
            if isinstance(state, dict):
                return self.state_class(**state)

            # If it's another Pydantic model, convert to dict first
            if hasattr(state, 'model_dump'):
                return self.state_class(**state.model_dump())

            raise StateValidationError(f"Cannot validate state of type: {type(state)}")
        except ValidationError as e:
            logger.error(f"State validation failed: {e}")
            raise StateValidationError(f"Invalid state format: {e}")
        except Exception as e:
            logger.error(f"Unexpected error in state validation: {e}")
            raise StateValidationError(f"State validation error: {e}")

    def transform_messages(self, messages: List[Union[BaseMessage, Dict[str, str]]]) -> List[Dict[str, str]]:
        """Transform messages to standard format."""
        try:
            converted = []
            for msg in messages:
                if isinstance(msg, HumanMessage):
                    converted.append({"role": "user", "content": msg.content})
                elif isinstance(msg, AIMessage):
                    converted.append({"role": "ai", "content": msg.content})
                elif isinstance(msg, dict):
                    if "role" not in msg or "content" not in msg:
                        raise StateValidationError("Message missing required fields")
                    converted.append(msg)
                else:
                    raise StateValidationError(f"Unsupported message type: {type(msg)}")
            return converted
        except Exception as e:
            logger.error(f"Message transformation failed: {e}")
            raise StateTransformError(f"Failed to transform messages: {e}")

    def transform_state_for_lambda(self, state: Dict[str, Any], config: Optional[RunnableConfig] = None) -> Dict[str, Any]:
        """Transform state for Lambda input."""
        try:
            # Validate state
            validated_state = self.validate_state(state)

            # Transform messages if present
            if hasattr(validated_state, 'messages'):
                validated_state.messages = self.transform_messages(validated_state.messages)

            # Convert to dict using model_dump() for Pydantic v2
            lambda_state = (
                validated_state.model_dump()
                if hasattr(validated_state, 'model_dump')
                else validated_state.dict()
            )

            # Add config and version information
            lambda_state["_metadata"] = {
                "version": getattr(validated_state, 'version', "1.0"),
                "config": self._serialize_config(config)
            }

            return lambda_state
        except Exception as e:
            logger.error(f"State transformation failed: {e}")
            raise StateTransformError(f"Failed to transform state for Lambda: {e}")

    def transform_lambda_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Transform Lambda response back to graph state."""
        try:
            if "updated_state" not in response:
                raise StateTransformError("Lambda response missing updated_state")

            updated_state = response["updated_state"]

            # Transform messages back if present
            if "messages" in updated_state:
                updated_state["messages"] = [
                    AIMessage(content=msg["content"]) if msg["role"] == "ai"
                    else HumanMessage(content=msg["content"])
                    for msg in updated_state["messages"]
                ]

            return updated_state
        except Exception as e:
            logger.error(f"Response transformation failed: {e}")
            raise StateTransformError(f"Failed to transform Lambda response: {e}")

    def _serialize_config(self, config: Optional[RunnableConfig]) -> Dict[str, Any]:
        """Serialize config to JSON-safe format."""
        if not config:
            return {}
        return {
            k: v for k, v in config.items()
            if k != "callbacks" and isinstance(v, (dict, list, str, int, float, bool))
        }

class ServerlessNode(Generic[StateType]):
    """Enhanced serverless node with state management."""

    def __init__(self,
                 node_id: str,
                 endpoint_url: str,
                 api_key: str,
                 state_class: Optional[type] = None):
        self.node_id = node_id
        self.endpoint_url = endpoint_url
        self.api_key = api_key
        self.state_manager = StateManager[StateType](state_class)

    async def __call__(self,
                       state: Dict[str, Any],
                       config: Optional[RunnableConfig] = None) -> Dict[str, Any]:
        """Enhanced call method with state management."""
        try:
            # Transform state for Lambda
            lambda_state = self.state_manager.transform_state_for_lambda(state, config)

            # Prepare request
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }

            payload = {"state": lambda_state}

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.endpoint_url,
                    json=payload,
                    headers=headers
                ) as response:
                    if response.status != 200:
                        raise NodeExecutionError(
                            f"Lambda call failed: {await response.text()}"
                        )

                    result = await response.json()

                    # Transform response
                    return self.state_manager.transform_lambda_response(result)

        except Exception as e:
            logger.error(f"Node execution failed: {e}")
            raise

class StateValidationError(Exception):
    """Raised when state validation fails."""
    pass

class StateTransformError(Exception):
    """Raised when state transformation fails."""
    pass

class NodeExecutionError(Exception):
    """Raised when node execution fails."""
    pass

def create_serverless_node(
    node_id: str,
    endpoint_url: str,
    api_key: str,
    state_class: Optional[type] = None
) -> RunnableLambda:
    """Enhanced factory function for serverless nodes."""
    node = ServerlessNode(
        node_id=node_id,
        endpoint_url=endpoint_url,
        api_key=api_key,
        state_class=state_class
    )

    return RunnableLambda(
        func=node
    ).with_retry(
        stop_after_attempt=3,
        wait_exponential_jitter=True,
        retry_if_exception_type=(
            aiohttp.ClientError,
            json.JSONDecodeError,
            StateValidationError,
            StateTransformError,
            NodeExecutionError
        )
    ).with_types(
        input_type=Dict[str, Any],
        output_type=Dict[str, Any]
    ).with_listeners(
        on_start=lambda run: logger.info(f"Starting node execution {run.id}"),
        on_end=lambda run: logger.info(f"Completed node execution {run.id}"),
        on_error=lambda run: logger.error(f"Node execution failed {run.id}: {run.error}")
    )

def upload_custom_node(
    node_code: str,
    metadata: dict,
    client_token: str,
    backend_url: str
) -> dict:
    """
    Upload a user's custom node code to your backend.

    The zip file should contain:
    - Your Python handler file
    - lambda_config.json specifying the handler details
    - Any additional dependencies
    """
    # Validate zip contains lambda_config.json
    try:
        zip_data = base64.b64decode(node_code)
        with zipfile.ZipFile(io.BytesIO(zip_data)) as zip_file:
            if "lambda_config.json" not in zip_file.namelist():
                raise ValueError("ZIP must contain lambda_config.json")

            # Read and validate config
            with zip_file.open("lambda_config.json") as config_file:
                config = json.load(config_file)

                required_fields = ["handler_file", "handler_function"]
                for field in required_fields:
                    if field not in config:
                        raise ValueError(f"lambda_config.json missing required field: {field}")

                # Verify handler file exists
                if config["handler_file"] not in zip_file.namelist():
                    raise ValueError(f"Handler file {config['handler_file']} not found in ZIP")

            # Validate directions if present
            if "directions" in metadata and not isinstance(metadata["directions"], str):
                raise ValueError("Directions must be a string")

    except (zipfile.BadZipFile, json.JSONDecodeError) as e:
        raise ValueError(f"Invalid ZIP file or lambda_config.json: {str(e)}")

    # Add config to metadata for backend processing
    metadata["lambda_config"] = config

    # Continue with existing upload logic
    headers = {
        "Authorization": f"Bearer {client_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "node_code": node_code,
        "metadata": metadata,
    }

    logger.debug(f"Uploading custom node with metadata keys: {list(metadata.keys())}")

    response = requests.post(f"{backend_url}/api/nodes/upload", json=payload, headers=headers)

    if response.status_code != 200:
        logger.error(f"Node upload failed: {response.text}")
        raise Exception(f"Node upload failed with HTTP {response.status_code}: {response.text}")

    data = response.json()
    logger.debug(f"Upload successful. Response keys: {list(data.keys())}")

    # data should at least contain { "node_id", "endpoint_url", "api_key" }
    return data
