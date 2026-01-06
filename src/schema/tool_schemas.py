from pydantic import BaseModel, Field

class SampleToolInput(BaseModel):
    """Input schema for the sample tool."""
    query: str = Field(..., description="The query string to process.")
    limit: int = Field(5, description="Maximum number of results to return.")

class AnotherToolInput(BaseModel):
    """Input schema for another tool."""
    item_id: int = Field(..., description="The ID of the item.")
    action: str = Field(..., description="The action to perform on the item.")
