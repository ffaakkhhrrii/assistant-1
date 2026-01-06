from langchain_core.tools import tool
from src.schema.tool_schemas import SampleToolInput, AnotherToolInput
from src.utils.api_caller import safe_api_call

@tool(args_schema=SampleToolInput)
async def sample_tool(query: str, limit: int = 5) -> str:
    """
    A sample tool that processes a query.
    Useful for demonstrating tool usage.
    """
    # Placeholder logic
    return f"Processed query: '{query}' with limit {limit}. (This is a mock response)"

@tool(args_schema=AnotherToolInput)
async def another_tool(item_id: int, action: str) -> str:
    """
    Another sample tool that performs an action on an item.
    """
    # Placeholder logic using the util
    # await safe_api_call("http://example.com", "POST", {"id": item_id, "action": action})
    return f"Performed action '{action}' on item {item_id}."

custom_tools = [sample_tool, another_tool]
