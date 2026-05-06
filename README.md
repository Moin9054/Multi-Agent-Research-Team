# Multi-Agent Research Team

A modular **Multi-Agent AI System** where specialized AI agents collaborate to research, analyze, strategize, and generate structured executive summaries on any topic.

This project demonstrates a **multi-agent orchestration architecture** using asynchronous execution, role-based prompting, and a modern Streamlit interface.

---

# 🚀 What This Application Does

The system simulates a collaborative AI research team.

Instead of relying on a single LLM response, the application divides responsibilities across multiple AI agents:

- **Researcher** → gathers background information
- **Analyst** → identifies risks, patterns, and opportunities
- **Strategist** → proposes actionable next steps
- **Coordinator** → combines all outputs into a final executive briefing

The result is a more structured and role-oriented workflow compared to traditional chatbot systems.

---

# 🧠 Multi-Agent Workflow

```text
User Topic
    ↓
Researcher Agent
    ↓
Analyst Agent + Strategist Agent (parallel execution)
    ↓
Coordinator Agent
    ↓
Final Executive Summary
```

---

# 👥 Agent Roles

## 🔹 Researcher
Provides:
- Topic background
- Key concepts
- Contextual understanding
- Suggested research directions

---

## 🔹 Analyst
Identifies:
- Risks
- Opportunities
- Trade-offs
- Key patterns

---

## 🔹 Strategist
Generates:
- Short-term actions
- Mid-term strategy
- Long-term roadmap
- Success metrics

---

## 🔹 Coordinator
Synthesizes:
- Executive summary
- Consolidated insights
- Final recommendations

---

# ⚡ Key Features

- Multi-agent AI architecture
- Asynchronous orchestration using `asyncio`
- Parallel agent execution
- OpenRouter LLM integration
- Streamlit-based modern UI
- FastAPI endpoint support
- Modular and extensible design
- Copy-to-clipboard support
- Recent run history tracking

---

# 🛠️ Tech Stack

## Frontend
- Streamlit

## Backend
- Python
- Asyncio
- aiohttp
- FastAPI

## LLM
- OpenRouter
- LLaMA 3.1 8B Instruct

## Optional Visualization
- NetworkX

---

# 📁 Project Structure

```text
Multi-agent-research/
│
├── app/
│   ├── __init__.py
│   ├── agents.py          # Agent definitions and orchestration
│   ├── api.py             # FastAPI endpoint
│   ├── graph.py           # Agent workflow graph
│   └── utils.py           # OpenRouter API utility
│
├── streamlit_app.py       # Streamlit frontend
├── requirements.txt
└── README.md
```

---

# ⚙️ How It Works

## 1️⃣ User Inputs a Topic

Example:

```text
How to increase company revenue
```

---

## 2️⃣ Researcher Agent Runs First

The researcher gathers foundational knowledge about the topic.

---

## 3️⃣ Analyst and Strategist Run in Parallel

Using asynchronous execution:

- Analyst extracts insights
- Strategist generates action plans

This improves efficiency and mimics real-world team collaboration.

---

## 4️⃣ Coordinator Generates Final Briefing

The coordinator consolidates all outputs into a final executive summary.

---

# 📦 Example Use Cases

- Business strategy generation
- Market research
- Product planning
- AI trend analysis
- Startup growth strategy
- Competitive analysis
- Executive briefing automation

---

# 🔧 Installation & Setup

## 1️⃣ Clone Repository

```bash
git clone <your_repo_url>
cd Multi-agent-research
```

---

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux

```bash
python -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Create `.env` File

```env
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_MODEL=meta-llama/llama-3.1-8b-instruct
```

---

# ▶️ Running the Streamlit App

```bash
streamlit run streamlit_app.py
```

The app will open in your browser:

```text
http://localhost:8501
```

---

# 🌐 Running the FastAPI Server (Optional)

```bash
uvicorn app.api:app --reload
```

Swagger Docs:

```text
http://127.0.0.1:8000/docs
```

---

# 📊 Example Topics

- Impact of AI on Global Education
- Revenue Growth Strategy for SaaS Companies
- Future of Electric Vehicles
- AI Adoption in Healthcare
- Digital Transformation in Banking

---

# ⚠️ Limitations

- No persistent memory between sessions
- No real-time web search
- Responses depend on LLM reasoning only
- No external tool integrations

---

# 🔮 Future Improvements

- Add web search tools
- Add memory and conversation persistence
- Integrate LangGraph or CrewAI
- Add PDF export
- Add citation support
- Add agent-to-agent feedback loops

---

# 🧾 Final Summary

This project demonstrates how multiple AI agents can collaboratively solve complex problems through role-based reasoning, asynchronous orchestration, and structured synthesis.

It showcases concepts commonly used in modern AI systems such as:
- multi-agent workflows
- AI orchestration
- async execution
- modular LLM architectures
