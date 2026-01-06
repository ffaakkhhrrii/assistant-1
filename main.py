from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage
from src.agent_graph import agent_graph
import json
import asyncio

app = FastAPI(title="LangGraph Gemini Agent", version="1.0.0")

class ChatRequest(BaseModel):
    message: str
    id: str

async def generate_response(message: str, thread_id: str):
    """
    Generator that runs the agent graph and yields chunks.
    Note: LangGraph streaming behavior depends on how you iterate.
    Here we stream the events.
    """
    inputs = {"messages": [HumanMessage(content=message)]}
    config = {"configurable": {"thread_id": thread_id}}
    
    # Stream events from the graph
    # config={"recursion_limit": 50}
    async for event in agent_graph.astream_events(inputs, config=config, version="v1"):
        kind = event["event"]
        
        # Filter for chat model output (on_chat_model_stream) to stream tokens
        if kind == "on_chat_model_stream":
            content = event["data"]["chunk"].content
            if content:
                yield content

@app.post("/stream")
async def stream_agent(request: ChatRequest):
    """
    Endpoint to interact with the agent via streaming.
    """
    return StreamingResponse(generate_response(request.message, request.id), media_type="text/plain")

@app.get("/health")
def health_check():
    return {"status": "ok"}
