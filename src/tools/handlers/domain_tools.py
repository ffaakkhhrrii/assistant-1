from langchain_core.tools import tool

@tool
def get_spend() -> str:
    """Get spend data."""
    return "Spend data placeholder"

@tool
def get_requisition() -> str:
    """Get requisition data."""
    return "Requisition data placeholder"

@tool
def get_contract() -> str:
    """Get contract data."""
    return "Contract data placeholder"

@tool
def get_order() -> str:
    """Get order data."""
    return "Order data placeholder"

@tool
def get_supplier() -> str:
    """Get supplier data."""
    return "Supplier data placeholder"

@tool
def get_tender() -> str:
    """Get tender data."""
    return "Tender data placeholder"

@tool
def get_commodity_group() -> str:
    """Get commodity group data."""
    return "Commodity group data placeholder"

@tool
def get_vendor_quality() -> str:
    """Get vendor quality data."""
    return "Vendor quality data placeholder"

@tool
def post_draft_pr_planning() -> str:
    """Post draft PR planning."""
    return "Posted draft PR planning placeholder"
