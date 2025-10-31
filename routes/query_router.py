from fastapi import APIRouter, Body
from pydantic import BaseModel
from typing import Any, Dict

# ---- Import your agent runners here ----
from agents.github_agent import run_github_agent
from agents.linear_agent import run_linear_agent
from router_logic.llm_router import route_to_agent   # Your LLM routing function

router = APIRouter()

# Add this mapping at the top of query_router.py
USER_MAP = {
    "alice": "user1",
    "bob": "user2"
}
# Request body schema
class QueryRequest(BaseModel):
    query: str

# Response model (optional)
class QueryResponse(BaseModel):
    agent: str
    user: str
    result: Any


@router.post("/query", response_model=QueryResponse)
async def handle_query(request: QueryRequest):
    """
    Accepts user query, routes to correct agent via LLM, returns agent result.
    """
    query = request.query

    # 🔥 Call the LLM router (it returns agent + user)
    routing_decision: Dict[str, str] = route_to_agent(query)
    agent = routing_decision.get("agent")
    user = routing_decision.get("user")
    user_key = USER_MAP.get(user, user)  # defaults to original if not found

    if agent == "github":
        result = run_github_agent(query, user_key)
    elif agent == "linear":
        result = run_linear_agent(query, user_key)
    else:
        result = "I cannot answer this question."

    return QueryResponse(
        agent=agent,
        user=user,
        result=result
    )
