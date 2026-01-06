import httpx
from typing import Dict, Any

async def safe_api_call(url: str, method: str = "GET", data: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Stub function to perform a safe API call.
    In a real scenario, this would handle timeouts, retries, and error logging.
    """
    try:
        async with httpx.AsyncClient() as client:
            if method.upper() == "GET":
                response = await client.get(url)
            elif method.upper() == "POST":
                response = await client.post(url, json=data)
            else:
                return {"error": f"Method {method} not supported"}
            
            response.raise_for_status()
            return response.json()
    except Exception as e:
        return {"error": str(e), "status": "failed"}

def format_response(data: Dict[str, Any]) -> str:
    """Helper to format API response data."""
    return str(data)
