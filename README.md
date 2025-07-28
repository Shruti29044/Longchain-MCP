# Complex LangChain MCP Project

### Features:
- LangChain agent with tools for Slack, PR summarization, and web search
- FastAPI server with `/agent` endpoint
- Environment-configured for OpenAI + Slack
- Extendable for GitHub integration

## Run Locally
```bash
pip install -r requirements.txt
uvicorn main:app --port 8080
```

## Example Task
POST `/agent` with JSON:
```json
{ "task": "Summarize this PR and notify Slack: <PR data here>" }
```