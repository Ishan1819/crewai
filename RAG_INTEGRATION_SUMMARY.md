# RAG Integration Summary

## Changes Made

### 1. **tools/github_rag.py** (Updated)

- Added complete `GitHubQA` class with:
  - `extract_repo()`: Extracts and indexes all code files from a GitHub repository
  - `_chunk()`: Chunks large files for better embedding
  - `ask()`: Answers questions using RAG with context from the repo
- Added `github_repo_qa()` CrewAI tool for repo-based Q&A
- Uses ChromaDB for vector storage and sentence-transformers for embeddings

### 2. **router_logic/llm_router.py** (Updated)

- Updated system prompt to support:
  - New agent type: `"github_rag"` for repo code questions
  - Repo extraction: Returns `"repo": "owner/repo"` when query is about specific repo code
- Updated `route_to_agent()` to return repo name in routing decision

### 3. **routes/query_router.py** (Updated)

- Imported `github_repo_qa` tool
- Updated `QueryResponse` model to include optional `repo` field
- Added routing logic for `"github_rag"` agent:
  ```python
  elif agent == "github_rag" and repo:
      result = github_repo_qa(user_key, repo, query)
  ```

### 4. **requirements.txt** (Already has dependencies)

- `chromadb` - Vector database
- `sentence-transformers` - Text embeddings

## How It Works

1. **User asks a code-related question** (e.g., "What does the main.py file do in Ishan1819/crewai?")

2. **Router detects**:

   - Agent: `"github_rag"`
   - User: `"alice"` or `"bob"`
   - Repo: `"Ishan1819/crewai"`

3. **RAG Process**:
   - Extracts all code files from the repo
   - Chunks and embeds them into ChromaDB
   - Retrieves relevant code snippets for the question
   - Sends context + question to Gemini
   - Returns detailed answer with file references

## Example Queries

- "What is the authentication logic in Ishan1819/crewai?"
- "Show me how the GitHub agent works in alice's crewai repo"
- "Explain the router logic in bob's repository Ishan1819/crewai"

## Testing

To test the RAG integration:

```bash
# Start the server
python main.py

# Send a query via POST /api/query
{
  "query": "What does the main.py file do in Ishan1819/crewai for alice?"
}
```

The system will:

1. Route to `github_rag` agent
2. Extract repo: `Ishan1819/crewai`
3. Use Alice's GitHub token (USER1)
4. Index the entire repo
5. Answer the question with code context

## Notes

- First query to a repo will be slower (indexing time)
- Subsequent queries to the same repo are faster (cached embeddings)
- Supports Python, JavaScript, TypeScript, Java, C++, and many more file types
- Maximum file size: 500KB per file
- Chunk size: 1000 characters with 200 character overlap
