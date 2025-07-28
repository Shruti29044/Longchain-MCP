from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain.prompts import PromptTemplate
import os
import requests

# Load .env variables
load_dotenv()

# Load LLM: OpenAI or Ollama
provider = os.getenv("LLM_PROVIDER", "openai").lower()

if provider == "ollama":
    from langchain_community.llms import Ollama
    llm = Ollama(model="llama3")
else:
    from langchain_openai import OpenAI
    llm = OpenAI(temperature=0)

# Slack webhook
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

# FastAPI app
app = FastAPI()

# ----- Tools -----
def suggest_pr_template(changed_files: str) -> str:
    if "docs/" in changed_files:
        return "📄 Documentation Update"
    elif "test/" in changed_files:
        return "🧪 Test Improvements"
    else:
        return "✨ Feature Implementation"

def notify_slack(message: str) -> str:
    if not SLACK_WEBHOOK_URL:
        return "❌ Slack webhook not configured."
    payload = {"text": message, "mrkdwn": True}
    response = requests.post(SLACK_WEBHOOK_URL, json=payload)
    return f"✅ Sent to Slack: {response.status_code}"

def summarize_pr(content: str) -> str:
    template = PromptTemplate.from_template("""
Summarize this pull request for Slack:
- Use bullet points
- Add emojis where appropriate
- Keep it under 5 lines

Pull Request Content:
{content}
""")
    prompt = template.format(content=content)
    return llm.invoke(prompt)

# Register tools
tools = [
    Tool.from_function(
        name="SuggestPRTemplate",
        func=suggest_pr_template,
        description="Suggest a PR label based on changed files",
    ),
    Tool.from_function(
        name="NotifySlack",
        func=notify_slack,
        description="Send a message to Slack via webhook",
    ),
    Tool.from_function(
        name="SummarizePR",
        func=summarize_pr,
        description="Summarize a pull request for Slack",
    ),
]

# Initialize agent
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# FastAPI schema
class AgentRequest(BaseModel):
    task: str

@app.post("/agent")
async def run_agent(request: AgentRequest):
    result = agent.invoke({"input": request.task})
    return {"result": result}
