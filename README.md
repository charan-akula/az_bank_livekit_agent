# LiveKit AI Voice Agent Platform

This project is an **AI-powered real-time voice + chat interaction platform** built on **LiveKit** and modern AI infrastructure. It enables natural, two-way conversations where intelligent agents can listen, understand, reason, and respond instantly.

This platform powers an intelligent AI support agent designed specifically for **AZ Bank customer service automation**. It enables real-time voice and chat assistance that can verify users, support by banking information,  retrieve account information, resolve issues, and automatically create support tickets.

The system integrates:

- STT → LLM → TTS pipeline
- Retrieval-Augmented Generation (RAG)
- n8n workflow automation
- MCP tool connectivity
- Banking workflow integrations

It is designed for real-world enterprise use cases such as:

- Banking customer support
- Customer verification
- OTP workflows
- Jira ticket automation
- Real-time conversational assistance

---

# 🏗️ Architecture Overview

The system consists of three main components:

### Frontend
React (Vite) interface for real-time user interaction.

### Backend
FastAPI service for:
- Authentication
- Token generation
- API orchestration

### Agent
LiveKit AI voice agent responsible for:
- Speech processing
- Reasoning
- Tool calling
- Workflow triggering

---

# ✅ Prerequisites

Install these before setup:

- Node.js 18+
- Python 3.11+
- UV package manager (recommended) or pip
- LiveKit account
- n8n account (cloud or self-hosted)

---

# 🚀 Setup Guide

---

## 1️⃣ Clone Repository

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd az_bank_livekit_agent
```

---

## 2️⃣ Create Environment File

Create a `.env` file in the project root and add:

```
# LiveKit Agent Configuration

LIVEKIT_URL=wss://your-livekit-server.livekit.cloud
LIVEKIT_API_KEY=your_livekit_api_key_here
LIVEKIT_API_SECRET=your_livekit_api_secret_here

# n8n MCP Integration
N8N_MCP_URL=https://your-n8n-instance.com/mcp/webhook

# RAG Pipeline
PDF_PATH=./rag/az_bank.pdf

# Google AI (Gemini embeddings/LLM)
GOOGLE_API_KEY=your_google_api_key_here
```

⚠️ **Never commit `.env` files**

---

## 3️⃣ Install Dependencies

Run from project root:

```bash
uv pip install -r requirements.txt
```

---

## 4️⃣ LiveKit Setup

1. Create account
2. Create project
3. Copy credentials:

- URL
- API Key
- API Secret

Paste into `.env`.

---

## 5️⃣ n8n Setup

You can either:

- Self-host n8n
**OR**
- Use 14-day free trial cloud version

Steps:

1. Create workflow
2. Import JSON:

```
agent/workflows/JIRA_WORKFLOW.json
```

3. Configure credentials:

Required integrations:

- Jira
- Google Sheets OR Excel
- Twilio (for OTP sending)

👉 Optional alternative  
Instead of Twilio, you can:

- Use Gmail node
- Send OTP via email
- Select Gmail column from Sheets

4. Copy MCP webhook URL into `.env`:

```
N8N_MCP_URL=https://your-n8n-instance.com/mcp/webhook
```

---

## 6️⃣ Data Store Setup (Sheets / Excel)

Create a sheet with **exact column names**:

- Customer ID
- Account Holder Name
- Account Number
- IFSC Code
- Phone Number (India)
- Email
- Current OTP
- Current Jira ID
- Current Issue
- Current Key

⚠️ Column names must match exactly.

---

# ▶️ Run Application

Start services in order:

---

### 1️⃣ Start Backend

```bash
uvicorn backend.main:app --reload
```

---

### 2️⃣ Start Agent

```bash
python agent/lkt_agent.py
```

---

### 3️⃣ Start Frontend

```bash
cd frontend
npm install
npm run dev
```

---

🌐 Open in browser:

```
http://localhost:5173
```

---

# 🔐 Security Notes

- `.env` is ignored by Git
- Never expose API keys in frontend
- Rotate credentials if compromised
- Do not upload vector DB or secrets

---

# 📦 Features

- Real-time Voice + Chat AI Agent
- RAG knowledge retrieval
- LiveKit streaming voice
- Tool calling via MCP
- Workflow automation via n8n
- OTP verification
- Jira ticket automation
- Banking workflow orchestration

---

# 📌 Use Cases

- AI customer support agent
- Automated banking assistant
- Voice-based helpdesk
- Identity verification systems
- Conversational workflow automation
- Enterprise support bots

---

# 👤 Author

**Charan**  
LiveKit AI Voice Agent Platform
