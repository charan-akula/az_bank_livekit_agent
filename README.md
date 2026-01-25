# LiveKit AI Voice Agent Platform

This project is a **AI voice interaction platform** built on **LiveKit**, designed to handle real-time voice conversations integrated with **n8n workflows**, **Jira automation**, and **Excel/Google Sheets–based data storage** to support the customers of a AZ Bank.

The system consists of:

* **Frontend**: React (Vite) web interface for user interaction
* **Backend**: FastAPI service for authentication, token generation, and API coordination
* **Agent**: LiveKit AI voice agent that processes conversations and triggers n8n workflows

This architecture enables real-time voice support use cases such as **banking support**, **customer verification**, **ticket creation**, and **workflow automation**.

---

## ✅ Prerequisites

Ensure the following are installed before starting:

* **Node.js 18+** and **npm**
* **Python 3.11+**
* **UV package manager** (recommended) or **pip**
* **LiveKit account**
* **n8n account**

---

## 🚀 Step-by-Step Setup

---

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd livekit-agent
```

---

### 2️⃣ Create Environment File

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

`.env.example`

```
LIVEKIT_URL=
LIVEKIT_API_KEY=
LIVEKIT_API_SECRET=
N8N_MCP_URL=
```

⚠️ Never commit `.env` files to GitHub

---

### 3️⃣ LiveKit Setup

1. Go to 👉 [https://livekit.io/](https://livekit.io/)
2. Sign up or log in
3. Create a new project
4. Copy the following:

   * LiveKit URL
   * API Key
   * API Secret

Update your root `.env` file:

```
LIVEKIT_URL=wss://xxxx.livekit.cloud
LIVEKIT_API_KEY=xxxxxxxx
LIVEKIT_API_SECRET=xxxxxxxx
```

These credentials are used by:

* Backend
* Agent

---

### 4️⃣ n8n Setup

1. Go to 👉 [https://n8n.io/](https://n8n.io/)
2. Sign up or log in
3. Create a new workflow
4. Import the workflow JSON located at:

```
agent/workflows/JIRA_WORKFLOW.json
```

5. Configure required credentials inside n8n:

   * Jira
   * Google Sheets or Excel
   * Any additional API tokens

6. Copy the Webhook / MCP URL

Update `.env`:

```
N8N_MCP_URL=https://your-n8n-url/webhook/xxxx
```

---

### 5️⃣ Excel / Google Sheets Setup (Data Store)

Currently, the application uses Excel or Google Sheets as the data store.

Create a sheet with the **exact column names** below:

* Customer ID
* Account Holder Name
* Account Number
* IFSC Code
* Phone Number (India)
* Email
* Current OTP
* Current Jira ID
* Current Issue
* Current Key

⚠️ Column names must match exactly for workflows to function correctly.

---

### 6️⃣ Backend Setup (FastAPI)

```bash
cd backend
```

Install dependencies:

```bash
uv pip install -r requirements.txt
```

Run the backend:

```bash
uvicorn main:app --reload
```

Backend will be available at:

```
http://localhost:8000
```

---

### 7️⃣ Agent Setup (LiveKit AI Agent)

```bash
cd agent
```

Install dependencies:

```bash
uv pip install -r requirements.txt
```

Start the agent:

```bash
python lkt_agent.py
```

The agent connects to:

* LiveKit
* n8n
* Backend

---

### 8️⃣ Frontend Setup (React + Vite)

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the frontend:

```bash
npm run dev
```

Frontend will be available at:

```
http://localhost:5173/
```

---

## ▶️ Final Run Order (IMPORTANT)

Start the services in the following order:

### 1️⃣ Backend

```bash
cd backend
uvicorn main:app --reload
```

### 2️⃣ Agent

```bash
cd agent
python lkt_agent.py
```

### 3️⃣ Frontend

```bash
cd frontend
npm run dev
```

🌐 Open in Browser:

```
http://localhost:5173/
```

---

## 🔐 Security Notes

* `.env` files are excluded via `.gitignore`
* Do not expose secrets in frontend code
* Rotate LiveKit and n8n credentials if compromised

---

## 📌 Use Cases

* AI-powered voice-based customer support
* Automated Jira ticket creation
* Banking and KYC verification flows
* Workflow orchestration via n8n
* Real-time voice interaction using LiveKit

---

## 👤 Author

**Charan** – LiveKit AI Voice Agent Platform
