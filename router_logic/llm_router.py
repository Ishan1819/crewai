import os
import json
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
        prompt = system_prompt.strip() + "\n" + user_query.strip()
        response = model.generate_content(prompt)

        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("```")[-2].strip()
        # parse JSON safely
        try:
            return json.loads(text)
        except:
            print("⚠️ Gemini returned non-JSON:", text)
            return {"agent": "none", "user": "unknown"}

    except Exception as e:
        print("❌ Gemini error:", e)
        return {"agent": "none", "user": "unknown"}


# -------------------- Router Logic --------------------
def route_to_agent(query: str):
    """
    Sends query to Gemini and returns routing decision
    """

    system_prompt = """
You are a strict routing engine for a multi-agent system.

### AGENT ROUTING RULES ###
- If query mentions GitHub terms (repo, PR, pull request, code, stars, commits, branches) → agent = "github"
- If query mentions Linear terms (issue, task, ticket, sprint, project, team) → agent = "linear"
- Otherwise → agent = "none"

### USER IDENTIFICATION RULES ###
- If "Alice" or "alice" in query → user = "alice"
- If "Bob" or "bob" in query → user = "bob"
- Otherwise → user = "unknown"

### OUTPUT ONLY THIS JSON (VERY STRICT) ###
{
  "agent": "github" | "linear" | "none",
  "user": "alice" | "bob" | "unknown"
}

No explanation. No markdown. Only JSON.
"""

    result = call_llm(system_prompt, query)

    # Force safe keys
    return {
        "agent": result.get("agent", "none"),
        "user": result.get("user", "unknown")
    }