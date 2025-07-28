# 🤖 LangChain MCP Agent (with Ollama & Slack Integration)

A powerful AI-driven backend that uses **LangChain agents** and **custom tools** to summarize GitHub Pull Requests and notify your team on **Slack** — built with **FastAPI**, integrated with **Ollama (LLaMA 3)** and optionally **OpenAI**.

---

## 📦 What Does This Project Do?

This project simulates an **MCP-style LangChain agent** that automates:

- ✅ **Summarizing PRs** in friendly, Slack-ready format
- ✅ **Suggesting PR labels** based on file types changed
- ✅ **Sending Slack notifications** using a webhook
- ✅ Running entirely **locally** using **Ollama**
- ✅ OR, optionally using **OpenAI API**

---

## 🧠 Architecture Overview

| Component          | Description                                                                 |
|-------------------|-----------------------------------------------------------------------------|
| 🧩 LangChain Agent | Uses a ReAct agent with multiple tools                                       |
| 🛠️ Tools           | Functions for PR summarization, labeling, Slack alerts                       |
| 💬 PromptTemplate  | A formatted instruction prompt for summarization                             |
| 🌐 Slack           | Sends updates using your Slack webhook                                       |
| 🧠 Ollama (LLaMA3) | The default local LLM provider (no internet or API key needed!)              |
| 🧠 OpenAI (optional) | You can switch to GPT-3.5/4 if needed via `.env`                             |

---

## 🚀 Features

- 🔁 Fully local LLM support via **Ollama**
- 🌍 Optionally switch to **OpenAI** by flipping one line in `.env`
- 📩 Instant **Slack alerts** after processing a PR
- ⚙️ Configurable and extendable tool system
- ⚡ FastAPI server with a clean `/agent` endpoint

---

## 📁 Project Structure

```bash
complex_langchain_mcp/
├── app/
│   ├── main.py             # Main FastAPI + LangChain app
│   ├── .env                # LLM provider + Slack webhook
│   ├── requirements.txt    # Dependencies
│   └── venv/               # Virtual environment (not pushed to Git)
````

---

## 🧪 How It Works

1. You send a POST request with a task:

   ```json
   {
     "task": "summarize this PR: fixed bug in api/utils.py"
   }
   ```

2. The **LangChain agent** processes the task:

   * Determines what tool to use
   * Uses the `SummarizePR` tool with a smart prompt
   * Then calls the `NotifySlack` tool to alert your team

3. A message like this appears on Slack:

   ```
   • 🐛 Bug fix alert!
   • Fixed an issue in `api/utils.py` 👀
   ```

---

## 🧰 Tech Stack

* **Python 3.11+**
* [FastAPI](https://fastapi.tiangolo.com/) — Backend framework
* [LangChain](https://www.langchain.com/) — Agent and tools
* [Ollama](https://ollama.com/) — Local LLM engine (used: `llama3`)
* [Slack Webhooks](https://api.slack.com/messaging/webhooks) — Messaging
* Optional: [OpenAI API](https://platform.openai.com/)

---

## ⚙️ Setup Instructions

### ✅ Prerequisites

* Python 3.11+
* [Ollama installed](https://ollama.com/download) with `llama3` pulled
* GitHub + Slack webhook URL

---

### 🧪 1. Clone the Repo

```bash
git clone https://github.com/Shruti29044/Longchain-MCP.git
cd Longchain-MCP/app
```

---

### 🧪 2. Create a Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # On Windows
```

---

### 🧪 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 🧪 4. Configure `.env`

```ini
LLM_PROVIDER=ollama
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/XXX/YYY/ZZZ
# Optional for OpenAI:
# OPENAI_API_KEY=sk-...
```

---

### 🧪 5. Start Ollama (if using it)

```bash
ollama run llama3
```

---

### 🧪 6. Run the Server

```bash
uvicorn main:app --reload --port 8080
```

---

### ✅ 7. Test the API

```bash
curl -X POST http://127.0.0.1:8080/agent ^
  -H "Content-Type: application/json" ^
  -d "{\"task\": \"summarize this PR: fixed bug in api/utils.py\"}"
```

---

## 🔄 Switching from Ollama to OpenAI

Just edit your `.env`:

```ini
LLM_PROVIDER=openai
OPENAI_API_KEY=your-key-here
```

That’s it! OpenAI will now be used automatically.

---

## 🚧 Challenges Faced

| Challenge                          | Solution                                                                |
| ---------------------------------- | ----------------------------------------------------------------------- |
| 🔐 Slack messages weren't posting  | Set the correct webhook URL in `.env` and made sure Slack app is active |
| ❌ Curl not working on Windows CMD  | Used PowerShell or split into one-line `curl` instead                   |
| 💥 FastAPI errors                  | Ensured `task` was sent in proper JSON via body                         |
| ⚠️ LangChain deprecation warnings  | Noted migration to LangGraph (but this still works fine)                |
| 🔁 Ollama model not found          | Had to run `ollama pull llama3` before `ollama run llama3`              |
| 🧠 Understanding LangChain tooling | Took time to understand `Tool`, `PromptTemplate`, `initialize_agent`    |

---

## 📌 Example Slack Message

```
• 🐛 Bug fix alert! 🔧
• Fixed an issue in `api/utils.py` 👀
```

---

## 🙌 Future Ideas

* GitHub API integration (auto-fetch PRs)
* Use LangGraph instead of ReAct agent
* Add support for Jira, Discord, etc.
* Automatic code quality summaries

---

## 📜 License

MIT — use it freely, improve it, and share with the community!

---

## 💬 Made with ❤️ by Shruti

