import os
import json
import re
import google.generativeai as genai

# -------------------- Configure Gemini --------------------
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# -------------------- LLM Call Wrapper --------------------
def call_llm(system_prompt: str, user_query: str) -> dict:
    """
    Calls Gemini for routing and returns parsed JSON dict.
    """

    model = genai.GenerativeModel("gemini-2.5-flash")

    try:
        # Combine system and user prompt as a single user message
        prompt = system_prompt.strip() + "\n\n" + user_query.strip()
        response = model.generate_content(prompt)

        text = response.text.strip()
        
        # Remove markdown code blocks if present
        if "```" in text:
            # Extract content between code blocks
            match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
            if match:
                text = match.group(1).strip()
            else:
                # Fallback: try to find JSON object
                match = re.search(r'\{.*?\}', text, re.DOTALL)
                if match:
                    text = match.group(0).strip()
        
        # Parse JSON safely
        try:
            parsed = json.loads(text)
            return parsed
        except json.JSONDecodeError as je:
            print(f"⚠️ Gemini returned non-JSON: {text}")
            print(f"   JSON Error: {je}")
            return {"agent": "none", "user": "unknown"}

    except Exception as e:
        print(f"❌ Gemini error: {e}")
        return {"agent": "none", "user": "unknown"}


# -------------------- Router Logic --------------------
def route_to_agent(query: str) -> dict:
    """
    Sends query to Gemini and returns routing decision.
    
    Returns:
        dict with keys:
            - agent: "github" | "linear" | "none"
            - user: "alice" | "bob" | "unknown"
    """

    system_prompt = """
You are a strict routing engine for a multi-agent system.

### AGENT ROUTING RULES ###
- If query mentions GitHub terms (repo, PR, pull request, code, stars, commits, branches, repository) → agent = "github"
- If query mentions Linear terms (issue, task, ticket, sprint, project, team, Linear) → agent = "linear"
- Otherwise → agent = "none"

### USER IDENTIFICATION RULES ###
- If "Alice" or "alice" appears in query → user = "alice"
- If "Bob" or "bob" appears in query → user = "bob"
- Otherwise → user = "unknown"

### OUTPUT FORMAT ###
Return ONLY a valid JSON object with this exact structure:
{
  "agent": "github",
  "user": "alice"
}

CRITICAL: Return ONLY the JSON object. No explanations, no markdown, no extra text.
"""

    result = call_llm(system_prompt, f"Query: {query}")

    # Validate and return with safe defaults
    agent = result.get("agent", "none")
    user = result.get("user", "unknown")
    
    # Normalize values
    if agent not in ["github", "linear", "none"]:
        agent = "none"
    if user not in ["alice", "bob", "unknown"]:
        user = "unknown"
    
    return {
        "agent": agent,
        "user": user
    }


# -------------------- Test Function --------------------
if __name__ == "__main__":
    # Test cases
    test_queries = [
        "Show me the pull requests of Alice"
    ]
    
    print("Testing Router:\n")
    for query in test_queries:
        result = route_to_agent(query)
        print(f"Query: {query}")
        print(f"Result: {result}\n")