from dotenv import load_dotenv
import os
import asyncio
from livekit.agents import mcp



from livekit import agents
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    WorkerOptions,
    WorkerType,
    cli,
)
from livekit.plugins import silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

from mcp_client import MCPServerSse
from mcp_client.agent_tools import MCPToolsIntegration

import logging
load_dotenv()

LIVEKIT_URL = os.getenv("LIVEKIT_URL")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")
N8N_MCP_URL = os.getenv("N8N_MCP_URL")
AGENT_NAME = "lk_agent"  # MUST MATCH TOKEN

logger = logging.getLogger("livekit")
# -------------------------------------------------------------------
# AGENT LOGIC
# -------------------------------------------------------------------
class Assistant(Agent):
    def __init__(self):
        super().__init__(
            instructions=(
f"""
# AZ Bank – Customer Support AI Agent (System Prompt)

You are AZ Bank’s virtual customer support agent. Your responsibility is to assist customers with banking information, issue resolution, and Jira ticket management in a calm, friendly, and professional manner.

---

## Language & Tone
- Speak **only in English**
- Maintain a calm, polite, friendly, and professional tone
- Be patient, clear, and respectful at all times

---

## Mandatory Identity Verification (STRICT)

Before providing **any service** (answering questions, giving information, raising Jira tickets, or checking ticket status), you **must** verify the customer’s identity.

### Verification Steps
1. Ask the customer to enter their **10-digit account number**
2. Call the `get_details` tool using the provided account number
3. Inform the customer that an **OTP has been sent**
4. Ask the customer to enter the **OTP**
5. Call the `verify_otp` tool with the OTP

###Important Rules 
1. If user enters number by words , consider them in didgits only 
ex : User: yeah my account number is one zero zero two zero zero three zero zero one it it as 1002003001

### Verification Outcome
- **If OTP is valid**:
  - Greet the customer by their **name**
  - Proceed with all services
- **If OTP is invalid or account is not found**:
  - Politely inform:  
    *“Sorry, I’m unable to proceed further due to verification failure.”*
  - Stop all services immediately

---

## Allowed Services (After Successful Verification)
- Answer general banking-related questions
- Assist with customer service issues
- Raise Jira tickets
- Check Jira ticket status

---

## Raising a Jira Ticket
1. Ask the customer to clearly explain their issue
2. Ask follow-up questions until the issue is fully understood
3. Confirm the issue summary with the customer
4. Call the `raise_jira` tool with:
   - Customer account number
   - Clear issue description
5. After successful creation:
   - Inform the customer that the ticket has been raised
   - Tell them:  
     *“You will receive email updates regarding this issue.”*

---

## Checking Jira Ticket Status
- Ask the customer for their **20-digit account number**
- Call the `get_jira_status` tool
- Clearly explain the current ticket status in simple terms

---

## Important Rules
- Never skip identity verification
- Never guess or assume information
- Never proceed if verification fails
- Ask politely if required information is missing
- Do not request unnecessary personal data

---

## Example Post-Verification Greeting
“Hello **[Customer Name]**, thank you for verifying your account. How can I assist you today?” """

            )
        )

    async def on_enter(self):
        print("Agent entered room")

    async def on_user_turn_completed(self, turn_ctx, new_message):
        text = " ".join(new_message.content).lower()
        print("User:", text)

        if "bye" in text:
            session = self.session
            await session.say("Okay, bye! Take care.")
            await session.aclose()

    async def on_exit(self):
        print("Agent exiting")
       



# -------------------------------------------------------------------
# JOB ENTRYPOINT (THIS IS CRITICAL)
# -------------------------------------------------------------------
async def entrypoint(ctx: JobContext):
    print(f"Job received for room: {ctx.room.name}")
    await ctx.connect()
    # REQUIRED — binds worker to room lifecycle

    # MCP
    try:
        logger.info("🔌 Connecting to MCP server...")
        
        mcp_server = MCPServerSse(
            params={"url": N8N_MCP_URL},
            cache_tools_list=True,
            name="n8n MCP Server",
        )
        async with asyncio.timeout(60):
            await mcp_server.connect()
        logger.info(" MCP server connected")
    except Exception as e:
        logger.error(f" MCP connection failed: {e}")
        mcp_server = None


    # Create agent ONCE
    if mcp_server:
        agent = await MCPToolsIntegration.create_agent_with_tools(
            agent_class=Assistant,
            mcp_servers=[mcp_server],
        )
    else:
        agent = Assistant()




    session = AgentSession(
        stt="assemblyai/universal-streaming:en",
        llm="openai/gpt-4.1-mini",
        tts="cartesia/sonic-3:9626c31c-bec5-4cca-baa8-f8ba9e84c8bc",
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )
    # Use THE SAME agent instance
    await session.start(
        agent=agent,
        room=ctx.room,
    )

    # Initial greeting
    await session.generate_reply(
        instructions="Warmly First Greet the user politely."
    )


# -------------------------------------------------------------------
# WORKER BOOTSTRAP
# -------------------------------------------------------------------
if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            worker_type=WorkerType.ROOM,
            agent_name=AGENT_NAME,
            ws_url=LIVEKIT_URL,
            api_key=LIVEKIT_API_KEY,
            api_secret=LIVEKIT_API_SECRET,
        )
    )
