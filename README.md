# Sovereign Agent Lab

A multi-agent AI system exploring **modern agent architectures** using:
- LangGraph tool-using research agents
- Rasa CALM structured conversational agents
- MCP (Model Context Protocol) tool sharing
- Context engineering and prompt robustness experiments

This project demonstrates how different AI system designs trade off between:
- flexibility (LangGraph agents)
- control and reliability (Rasa CALM)
- interoperability (MCP tools)

---

## 🚀 Key Features

### 1. LangGraph Research Agent
A tool-using agent built with LangGraph that:
- Plans and executes multi-step reasoning tasks
- Uses external tools (weather, cost estimation, venue checks, flyer generation)
- Handles failure modes and partial tool success
- Demonstrates agent loop control vs static prompting

### 2. MCP Tool Server (Shared Tool Layer)
A lightweight tool interface exposing:
- `search_venues`
- `get_venue_details`

These tools are dynamically discoverable and shared across:
- LangGraph agents
- external MCP clients
- future systems

### 3. Rasa CALM Conversation Agent
A structured conversational assistant for booking workflows:
- Slot extraction via LLM (`from_llm`)
- Flow-based dialogue control
- Deterministic business rules (deposit limits, validation)
- Safe handling of out-of-scope inputs

### 4. Context Engineering Experiments
Evaluation of how:
- prompt structure (plain vs XML vs sandwich formatting)
- model size differences
- distractor information

affect model correctness and stability.

---

---

## 🧩 Project Structure

```text
multi-agent-ai-event-orchestrator/
├── conversation_agent/
├    ├── config/
│          ├── config.yml
│          ├── endpoints.yml
│          ├── domain.yml
│    ├── guardrails/
├          ├──booking_policy.py
│    ├── pyproject.toml
│    ├── uv.lock
│    ├── .python-version
│ 
├── evaluation/
│      ├── context_engineering/
│            ├── ex1.py
│            ├── ex2.py
│            ├── ex3.py
│            ├── ex4.py
│
├── sovereign_agent/
│      ├── agents/
│           ├── research_agent.py
│      ├── tests/
│          ├── test_booking_policy.py
│      ├── tools/
│          ├── mcp_venue_server.py
│          ├── venue_tools.py
│
├── .env.example 
│
├── .gitignore
├── README.md
├── pyproject.toml
├── requirements.txt
├── smoke_test.py
├── uv.lock

```

---

## 🚀 Quick Start

```bash
uv sync
cp .env.example .env
```

---

## 🧪 What This Project Demonstrates

### Agent Architecture
- Separation of reasoning (LangGraph) vs structure (Rasa CALM)
- Shared tool layer via MCP
- Multi-agent system design patterns

### Tool-Driven AI Design
- Tools as first-class components
- Agents as orchestrators, not knowledge sources
- Shared state via external tool interfaces

### Reliability vs Flexibility Tradeoff
- LangGraph → adaptive reasoning, less deterministic
- Rasa CALM → deterministic, production-safe workflows

### Context Engineering
- Structured prompts improve constraint adherence
- Small models are significantly more formatting-sensitive
- Distractors degrade reasoning reliability

---

## 🧠 Key Insight

Modern AI systems are not single models.

They are **systems of control layers**:
- prompts define behavior
- tools define capability
- orchestration defines reliability

---

## 📌 Tech Stack

- Python 3.12+
- LangGraph
- Rasa Pro CALM
- MCP (Model Context Protocol)
- Nebius LLM API (OpenAI-compatible)
- OpenAI SDK
- Requests

---

## ⭐ Why This Project Matters

This repo demonstrates:

- real-world agent architecture (not toy chatbots)
- tool-use orchestration patterns
- structured conversation systems
- evaluation of LLM behavior under constraints
- production-style separation of concerns
```

---