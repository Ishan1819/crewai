# Quick Start Guide - RAG Integration

## Installation & Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Verify .env Configuration

Make sure your `.env` file has all required credentials:

```env
GITHUB_USERNAME_USER1=your_username
GITHUB_TOKEN_USER1=ghp_xxxxx
GITHUB_USERNAME_USER2=other_username
GITHUB_TOKEN_USER2=ghp_xxxxx
LINEAR_EMAIL_USER1=alice@example.com
LINEAR_API_KEY_USER1=lin_api_xxxxx
LINEAR_EMAIL_USER2=bob@example.com
LINEAR_API_KEY_USER2=lin_api_xxxxx
GEMINI_API_KEY=AIzaSyxxxxx
```

### 3. Start the Server

```bash
python main.py
```

You should see:

```
INFO:     Uvicorn running on http://127.0.0.1:8001 (Press CTRL+C to quit)
INFO:     Started reloader process
```

## Testing the RAG Integration

### Using curl (Command Line)

#### Test 1: RAG Code Query

```bash
curl -X POST "http://127.0.0.1:8001/api/query" \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"What does the main.py file do in Ishan1819/crewai for alice?\"}"
```

Expected response:

```json
{
  "agent": "github_rag",
  "user": "alice",
  "repo": "Ishan1819/crewai",
  "result": "📚 Answer for repo 'Ishan1819/crewai':\n[Detailed code analysis]"
}
```

#### Test 2: Regular GitHub Query

```bash
curl -X POST "http://127.0.0.1:8001/api/query" \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"Show alice's repositories\"}"
```

Expected response:

```json
{
  "agent": "github",
  "user": "alice",
  "repo": null,
  "result": "📂 Repositories for alice:\nrepo1\nrepo2\n..."
}
```

#### Test 3: Linear Query

```bash
curl -X POST "http://127.0.0.1:8001/api/query" \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"What are bob's linear issues?\"}"
```

Expected response:

```json
{
  "agent": "linear",
  "user": "bob",
  "repo": null,
  "result": "📝 Issues for bob:\nIssue 1 - In Progress\n..."
}
```

### Using Python Script

Run the test script:

```bash
python test_rag.py
```

### Using Swagger UI

1. Open browser: http://127.0.0.1:8001/docs
2. Click on **POST /api/query**
3. Click **Try it out**
4. Enter your query:
   ```json
   {
     "query": "Explain the github_agent.py in alice's Ishan1819/crewai repo"
   }
   ```
5. Click **Execute**

## Example Queries by Type

### 📚 RAG Queries (Code Analysis)

These will trigger the `github_rag` agent:

```
✅ "What does the main.py file do in Ishan1819/crewai for alice?"
✅ "Explain the router logic in bob's microsoft/vscode repository"
✅ "How is authentication implemented in alice's repo owner/name?"
✅ "Show me the API endpoints in bob's fastapi/fastapi repo"
✅ "What libraries are imported in alice's Ishan1819/crewai?"
```

### 🐙 GitHub Queries

These will trigger the `github` agent:

```
✅ "Show alice's repositories"
✅ "List bob's pull requests"
✅ "What repos has alice starred?"
✅ "Show branches in repo xyz for bob"
✅ "List commits in repo abc for alice"
```

### 📋 Linear Queries

These will trigger the `linear` agent:

```
✅ "List alice's issues"
✅ "Show bob's high priority tasks"
✅ "What are alice's in-progress tasks?"
✅ "Show bob's teams"
✅ "List alice's projects"
```

## Troubleshooting

### Issue: "Missing GitHub token for user X"

**Solution**: Check your `.env` file has `GITHUB_TOKEN_USER1` or `GITHUB_TOKEN_USER2`

### Issue: "System not ready. Repository needs to be extracted first."

**Solution**: This is normal for the first RAG query. The system is indexing the repo. Wait 10-30 seconds.

### Issue: "400 Content with system role is not supported"

**Solution**: Already fixed in the code. Make sure you're using the updated `llm_router.py`

### Issue: "⚠️ Gemini returned non-JSON"

**Solution**: Already fixed. The code now strips markdown code blocks from Gemini responses.

### Issue: Connection refused

**Solution**: Make sure the server is running with `python main.py`

### Issue: Slow RAG responses

**Solution**:

- First query to a repo is slow (indexing)
- Subsequent queries are faster
- Large repos take longer to index

## Performance Tips

1. **First Query**: Expect 10-60 seconds for repo indexing
2. **Subsequent Queries**: Should be fast (2-5 seconds)
3. **Large Repos**: May take longer or timeout (increase timeout if needed)
4. **Cache**: ChromaDB keeps embeddings in memory until server restart

## Next Steps

1. ✅ Test basic GitHub queries
2. ✅ Test basic Linear queries
3. ✅ Test RAG code analysis
4. 🔄 Integrate with your frontend
5. 🔄 Add more specialized agents
6. 🔄 Implement caching for faster responses

## API Documentation

Full interactive API docs available at:

- Swagger UI: http://127.0.0.1:8001/docs
- ReDoc: http://127.0.0.1:8001/redoc

## Support

If you encounter issues:

1. Check the console logs for errors
2. Verify all environment variables are set
3. Test with simple queries first
4. Check GitHub/Linear API rate limits
5. Verify API tokens are valid

---

**Happy Coding! 🚀**
