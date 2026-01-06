from src.tools.handlers.general import get_current_datetime
from src.tools.handlers.domain_tools import (
    get_spend, get_requisition, get_contract, get_order, 
    get_supplier, get_tender, get_commodity_group, 
    get_vendor_quality, post_draft_pr_planning
)

tool_registry = {
    "get_current_datetime": {
        "handler": get_current_datetime
    },
    "get_spend": {
        "activity": {
            "pre": "ipca.assistant.tool.spend.pre",
            "post": "ipca.assistant.tool.spend.post"
        },
        "handler": get_spend
    },
}

# Values list for binding to LLM
tools = [t["handler"] for t in tool_registry.values()]
