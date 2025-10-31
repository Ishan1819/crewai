# StackGen - Multi-Agent GitHub & Linear Assistant with RAG

A sophisticated multi-agent system that routes queries to specialized agents for GitHub, Linear, and code analysis using RAG (Retrieval-Augmented Generation).

## Features

### 🤖 Multi-Agent System

- **GitHub Agent**: Handles repository listings, PRs, issues, stars, branches, commits
- **Linear Agent**: Manages tasks, issues, projects, teams, priorities
- **RAG Agent**: Answers code-related questions by analyzing repository contents

### 🧠 Smart Routing

- Uses Gemini LLM to intelligently route queries to the appropriate agent
- Automatically detects user (Alice/Bob) from query
- Extracts repository names for code analysis queries

### 🔍 RAG-Powered Code Q&A

- Indexes entire repositories using vector embeddings
- Retrieves relevant code snippets for context
- Provides detailed answers with file references and code examples

## Architecture

```
stackgen/
├── agents/
│   ├── github_agent.py      # GitHub operations agent
│   └── linear_agent.py      # Linear operations agent
├── tools/
│   ├── github_tools.py      # GitHub CrewAI tools
│   ├── linear_tools.py      # Linear CrewAI tools
│   └── github_rag.py        # RAG-based repo Q&A tool
├── services/
│   ├── github_services.py   # GitHub API wrapper
│   └── linear_services.py   # Linear API wrapper
├── router_logic/
│   └── llm_router.py        # LLM-based routing logic
├── routes/
│   └── query_router.py      # FastAPI query endpoint
├── main.py                  # FastAPI application entry point
├── litellm_wrapper.py       # LiteLLM wrapper for CrewAI
└── .env                     # Environment variables
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file with the following:

```env
# Alice GitHub
GITHUB_USERNAME_USER1=your_username
GITHUB_TOKEN_USER1=your_github_token

# Bob GitHub
GITHUB_USERNAME_USER2=other_username
GITHUB_TOKEN_USER2=other_github_token

# Alice Linear
LINEAR_EMAIL_USER1=alice@example.com
LINEAR_API_KEY_USER1=your_linear_key

# Bob Linear
LINEAR_EMAIL_USER2=bob@example.com
LINEAR_API_KEY_USER2=other_linear_key

# Gemini Key
GEMINI_API_KEY=your_gemini_api_key
```

### 3. Run the Server

```bash
python main.py
```

Server will start at `http://127.0.0.1:8001`

## Usage

### API Endpoint

**POST** `/api/query`

**Request:**

```json
{
  "query": "What does the main.py file do in Ishan1819/crewai for alice?"
}
```

**Response:**

```json
{
  "agent": "github_rag",
  "user": "alice",
  "repo": "Ishan1819/crewai",
  "result": "📚 Answer for repo 'Ishan1819/crewai':\n[Detailed answer with code snippets]"
}
```

### Example Queries

#### GitHub Queries

```
- "Show alice's repositories"
- "List bob's pull requests"
- "What are alice's starred repos?"
- "Show branches in repo xyz for bob"
```

#### Linear Queries

```
- "List alice's issues"
- "Show bob's high priority tasks"
- "What teams is alice part of?"
- "Show in-progress issues for bob"
```

#### RAG Code Queries

```
- "What does the main.py file do in Ishan1819/crewai for alice?"
- "Explain the authentication logic in alice's repo owner/repo"
- "How does the router work in bob's Ishan1819/crewai repository?"
- "Show me the GitHub agent implementation in alice's crewai repo"
```

## Routing Logic

The system uses Gemini LLM to analyze queries and route them:

1. **github_rag**: Questions about code/files in a specific repository
2. **github**: General GitHub operations (repos, PRs, issues, etc.)
3. **linear**: Linear project management (tasks, issues, teams)
4. **none**: Unrecognized queries

## User Mapping

- `alice` → `USER1` environment variables
- `bob` → `USER2` environment variables

## Testing

Run the test script to verify the integration:

```bash
python test_rag.py
```

## RAG System Details

### Supported File Types

Python, JavaScript, TypeScript, Java, C++, C, C#, Ruby, Go, Rust, PHP, HTML, CSS, JSON, XML, YAML, Markdown, Shell scripts, SQL, and more.

### Vector Database

- **ChromaDB**: In-memory vector storage
- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)
- **Chunk Size**: 1000 characters with 200 character overlap

### Process Flow

1. Extract repository contents via GitHub API
2. Filter text-based files (ignoring binaries)
3. Chunk large files for better context
4. Generate embeddings using sentence-transformers
5. Store in ChromaDB with metadata
6. Query with semantic search
7. Retrieve top-k relevant chunks
8. Send context + question to Gemini
9. Return detailed answer

## Dependencies

- **FastAPI**: Web framework
- **CrewAI**: Multi-agent orchestration
- **PyGithub**: GitHub API client
- **google-generativeai**: Gemini LLM
- **chromadb**: Vector database
- **sentence-transformers**: Text embeddings
- **litellm**: LLM wrapper for CrewAI

## API Documentation

Once the server is running, visit:

- **Swagger UI**: http://127.0.0.1:8001/docs
- **ReDoc**: http://127.0.0.1:8001/redoc

## Notes

- First query to a repository will be slower due to indexing
- Subsequent queries to the same repo are faster (embeddings cached)
- Maximum file size: 500KB per file
- The system respects GitHub rate limits
- Make sure to use valid API tokens

## Error Handling

The system handles:

- Missing API tokens
- Invalid repository names
- API rate limits
- Network errors
- Malformed queries

## Security

⚠️ **Important**: Never commit your `.env` file to version control!

Add `.env` to `.gitignore`:

```
.env
__pycache__/
*.pyc
```

## License

[Your License Here]

## Contributing

[Your Contributing Guidelines Here]
