from langchain_core.runnables import RunnableLambda
from langgraph.prebuilt import ToolNode
from langchain_core.messages import ToolMessage, SystemMessage, AIMessage, HumanMessage


def handle_tool_error(state) -> dict:
    error = state.get("error")
    tool_calls = state["messages"][-1].tool_calls
    return {
        "messages": [
            ToolMessage(
                content=f"Error: {repr(error)}\n please fix your mistakes.",
                tool_call_id=tc["id"],
            )
            for tc in tool_calls
        ]
    }

def create_tool_node_with_fallback(tools: list) -> dict:
    return ToolNode(tools).with_fallbacks(
        [RunnableLambda(handle_tool_error)], exception_key="error"
    )


def convert_messages(messages):
    converted_messages = []
    for message in messages:
        if message.content:
            if isinstance(message, SystemMessage):
                converted_messages.append(("system", message.content))
            elif isinstance(message, AIMessage) or isinstance(message, ToolMessage):
                converted_messages.append(("ai", message.content))
            elif isinstance(message, HumanMessage):
                converted_messages.append(("human", message.content))
    return converted_messages

