import os
from typing import Annotated, Literal, TypedDict, List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages
from src.tools.registry import tools
from langgraph.checkpoint.memory import MemorySaver

# Define the state
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    current_step: str

# Initialize the model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

# Bind tools to the model
llm_with_tools = llm.bind_tools(tools)

def load_persona():
    try:
        with open("persona.md", "r") as f:
            return f.read()
    except FileNotFoundError:
        return "You are a helpful assistant."

SYSTEM_PROMPT = load_persona()

# --- Node Handlers ---

def prepare_agent(state: AgentState):
    """Sets the initial state or context if needed."""
    # Ensure system prompt is present
    messages = state["messages"]
    if not messages or (len(messages) > 0 and not hasattr(messages[0], 'type') or messages[0].type != 'system'):
         messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
         return {"messages": messages, "current_step": "prepare_agent"}
    
    return {"current_step": "prepare_agent"}

def call_agent(state: AgentState):
    """Invokes the LLM."""
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response], "current_step": "call_agent"}

def prepare_tools(state: AgentState):
    """Prepares for tool calls (e.g., logging hooks)."""
    # In a real app, you might parse the last message tool_calls 
    # and trigger 'pre' activity hooks defined in the registry here.
    return {"current_step": "prepare_tools"}

def finish_agent(state: AgentState):
    """Final step to clean up or log completion."""
    return {"current_step": "finish_agent"}

# --- Graph Logic ---

def should_continue(state: AgentState) -> Literal["prepare_tools", "finish_agent"]:
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "prepare_tools"
    return "finish_agent"

# Define the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("prepare_agent", prepare_agent)
workflow.add_node("call_agent", call_agent)
workflow.add_node("prepare_tools", prepare_tools)
workflow.add_node("tool_calls", ToolNode(tools)) # Using standard ToolNode for execution
workflow.add_node("finish_agent", finish_agent)

# Add edges
workflow.add_edge(START, "prepare_agent")
workflow.add_edge("prepare_agent", "call_agent")

workflow.add_conditional_edges(
    "call_agent",
    should_continue,
)

workflow.add_edge("prepare_tools", "tool_calls")
workflow.add_edge("tool_calls", "call_agent") # Loop back to agent to interpret result
workflow.add_edge("finish_agent", END)

# Compile
checkpointer = MemorySaver()
agent_graph = workflow.compile(checkpointer=checkpointer)
