# LMSystems SDK

The LMSystems SDK provides flexible interfaces for integrating and executing purchased graphs from the LMSystems marketplace in your Python applications. The SDK offers two main approaches:

1. **PurchasedGraph Class**: For seamless integration with LangGraph workflows
2. **LmsystemsClient**: For direct, low-level interaction with LMSystems graphs, offering more flexibility and control

### Try it in Colab

Get started quickly with our interactive Colab notebook:
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/18IGOYcnN_CZSuH6RBwIjeXq9zMMs59OQ?usp=sharing)

This notebook provides a hands-on introduction to the LMSystems SDK with ready-to-run examples.

## Installation

Install the package using pip:

```bash
pip install lmsystems==1.0.8
```


## Quick Start

### Using the Client SDK

The client SDK provides direct interaction with one LMSystems graphs (e.g. [Deep Research Agent](https://www.lmsystems.ai/graphs/groq-deep-research-agent-51/graph)):

```python
from lmsystems import (
    SyncLmsystemsClient,
    APIError
)
import os


def main():

    # Check for required environment variables
    api_key = os.environ.get("LMSYSTEMS_API_KEY")

    # Initialize client
    client = SyncLmsystemsClient(
        graph_name="groq-deep-research-agent-51",
        api_key=api_key
    )

    try:
        # Create a new thread
        thread = client.threads.create()
        print(f"Created thread with status: {client.get_thread_status(thread)}")

        # Example 1: Using default environment variables
        for chunk in client.stream_run(
            thread=thread,
            input = {
            "research_topic":"what are the best agent frameworks for building apps with llms?"
            },

            config =  {
                "configurable": {
                    "llm": "",
                    "tavily_api_key": "",
                    "groq_api_key": ""
                }
            },
            stream_mode=["messages", "updates"]
        ):
            print(f"Received chunk: {chunk}")
        # Example: Check final thread status
        final_status = client.get_thread_status(thread)
        print(f"Final thread status: {final_status}")

    except APIError as e:
        print(f"API Error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()
```

### Using PurchasedGraph with LangGraph

For integration with other Langgraph apps, you can plug Purchased Graphs in as a single node:

```python
from lmsystems.purchased_graph import PurchasedGraph
from langgraph.graph import StateGraph, START, MessagesState
import os
from dataclasses import dataclass


@dataclass
class ResearchState:
    research_topic: str


api_key = os.environ.get("LMSYSTEMS_API_KEY")

def main():

    # Initialize our purchased graph (which wraps RemoteGraph)
    purchased_graph = PurchasedGraph(
        graph_name="groq-deep-research-agent-51",
        api_key=api_key,
        default_state_values = {
        "research_topic":""
        },

        config =  {
            "configurable": {
                "llm": "llama-3.1-8b-instant",
                "tavily_api_key": "",
                "groq_api_key": ""
            }
        },
    )

    # Create parent graph and add our purchased graph as a node
    builder = StateGraph(ResearchState)
    builder.add_node("purchased_node", purchased_graph)
    builder.add_edge(START, "purchased_node")
    graph = builder.compile()

    # Use the parent graph - invoke
    result = graph.invoke({
        "research_topic": "what are the best agent frameworks for building apps with llms?"
    })
    print("Parent graph result:", result)

    # Use the parent graph - stream
    for chunk in graph.stream({
        "research_topic":"what are the best agent frameworks for building apps with llms?"
    }, subgraphs=True):  # Include outputs from our purchased graph
        print("Stream chunk:", chunk)

if __name__ == "__main__":
    main()


```

## Configuration

### API Keys and Configuration
The SDK now automatically handles configuration through your LMSystems account. To set up:

1. Create an account at [LMSystems](https://www.lmsystems.ai)
2. Navigate to your [account settings](https://www.lmsystems.ai/account)
3. Configure your API keys (OpenAI, Anthropic, etc.)
4. Generate your LMSystems API key

Your configured API keys and settings will be automatically used when running graphs - no need to include them in your code!

> **Note**: While configuration is handled automatically, you can still override settings programmatically if needed:
```python
# Optional: Override stored config
config = {
    "configurable": {
        "model": "gpt-4",
        "openai_api_key": "your-custom-key"
    }
}
purchased_graph = PurchasedGraph(
    graph_name="github-agent-6",
    api_key=os.environ.get("LMSYSTEMS_API_KEY"),
    config=config  # Optional override
)
```

Store your LMSystems API key securely using environment variables:
```bash
export LMSYSTEMS_API_KEY="your-api-key"
```

## API Reference

### LmsystemsClient Class

```python
LmsystemsClient.create(
    graph_name: str,
    api_key: str
)
```

Parameters:
- `graph_name`: Name of the graph to interact with
- `api_key`: Your LMSystems API key

Methods:
- `create_thread()`: Create a new thread for graph execution
- `create_run(thread, input)`: Create a new run within a thread
- `stream_run(thread, run)`: Stream the output of a run
- `get_run(thread, run)`: Get the status and result of a run
- `list_runs(thread)`: List all runs in a thread

### PurchasedGraph Class

```python
PurchasedGraph(
    graph_name: str,
    api_key: str,
    config: Optional[RunnableConfig] = None,
    default_state_values: Optional[dict[str, Any]] = None
)
```

Parameters:
- `graph_name`: Name of the purchased graph
- `api_key`: Your LMSystems API key
- `config`: Optional configuration for the graph
- `default_state_values`: Default values for required state parameters

Methods:
- `invoke()`: Execute the graph synchronously
- `ainvoke()`: Execute the graph asynchronously
- `stream()`: Stream graph outputs synchronously
- `astream()`: Stream graph outputs asynchronously

## Error Handling

The SDK provides specific exceptions for different error cases:
- `AuthenticationError`: API key or authentication issues
- `GraphError`: Graph execution or configuration issues
- `InputError`: Invalid input parameters
- `APIError`: Backend communication issues

Example error handling:
```python
from lmsystems.exceptions import (
    LmsystemsError,
    AuthenticationError,
    GraphError,
    InputError,
    APIError,
    GraphNotFoundError,
    GraphNotPurchasedError
)

try:
    result = graph.invoke(input_data)
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except GraphNotFoundError as e:
    print(f"Graph not found: {e}")
except GraphNotPurchasedError as e:
    print(f"Graph not purchased: {e}")
except GraphError as e:
    print(f"Graph execution failed: {e}")
except InputError as e:
    print(f"Invalid input: {e}")
except APIError as e:
    print(f"API communication error: {e}")
except LmsystemsError as e:
    print(f"General error: {e}")
```

## Stream Modes

The SDK supports different streaming modes through the `StreamMode` enum:

```python
from lmsystems import StreamMode

# Stream run with specific modes
async for chunk in client.stream_run(
    thread=thread,
    input=input_data,
    stream_mode=[
        StreamMode.MESSAGES,  # Stream message updates
        StreamMode.VALUES,    # Stream value updates from nodes
        StreamMode.UPDATES,   # Stream general state updates
        StreamMode.CUSTOM     # Stream custom-defined updates
    ]
):
    print(chunk)
```

Available stream modes:
- `StreamMode.MESSAGES`: Stream message updates from the graph
- `StreamMode.VALUES`: Stream value updates from graph nodes
- `StreamMode.UPDATES`: Stream general state updates
- `StreamMode.CUSTOM`: Stream custom-defined updates

## Support

For support, feature requests, or bug reports:
- Contact me at sean.sullivan3@yahoo.com