from langchain_core.tools import tool
from datetime import datetime

@tool
def get_current_datetime() -> str:
    """Get the current datetime."""
    return datetime.now().isoformat()
