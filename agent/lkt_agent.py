# from dotenv import load_dotenv
# import os
# import asyncio
# from livekit.agents import mcp



# from livekit import agents, api
# from livekit.agents import (
#     Agent,
#     AgentSession,
#     JobContext,
#     WorkerOptions,
#     WorkerType,
#     cli,
#     function_tool
# )
# from livekit.plugins import silero
# from livekit.plugins.turn_detector.multilingual import MultilingualModel

# from mcp_client import MCPServerSse
# from mcp_client.agent_tools import MCPToolsIntegration
# from livekit.api import ListParticipantsRequest
# from pathlib import Path
# from rag.query import get_top_matches
# from prompts import prompt

# import logging

# # Robust .env loading
# env_path = Path(__file__).parent / ".env"
# load_dotenv(dotenv_path=env_path)

# LIVEKIT_URL = os.getenv("LIVEKIT_URL")
# LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
# LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")
# N8N_MCP_URL = os.getenv("N8N_MCP_URL")
# AGENT_NAME = "lk_agent"  # MUST MATCH TOKEN

# print(f"LIVEKIT_URL: {LIVEKIT_URL}")
# print(f"LIVEKIT_API_KEY: {LIVEKIT_API_KEY}")
# print(f"LIVEKIT_API_SECRET: {LIVEKIT_API_SECRET}")
# print(f"N8N_MCP_URL: {N8N_MCP_URL}")
# print(f"AGENT_NAME: {AGENT_NAME}")



# logger = logging.getLogger("livekit")
# # -------------------------------------------------------------------
# # AGENT LOGIC
# # -------------------------------------------------------------------
# class Assistant(Agent):
#     def __init__(self):
#         super().__init__(
#             instructions=prompt)


#     async def on_enter(self):
#         print("Agent entered room")

#     async def on_user_turn_completed(self, turn_ctx, new_message):
#         text = " ".join(new_message.content).lower()
#         print("User:", text)

#         if "bye" in text:
#             session = self.session
#             await session.say("Okay, bye! Take care.")
#             await session.aclose()

#     @function_tool
#     async def get_az_bank_info(
#         query: str,
#         k: int = 3,
#     ):
#         """Used to get the information from the AZ bank documents"""
#         return get_top_matches(query, k)
    
#     async def on_exit(self):
#         print("Agent exiting")
       


# # -------------------------------------------------------------------
# # JOB ENTRYPOINT (THIS IS CRITICAL)
# # -------------------------------------------------------------------
# async def entrypoint(ctx: JobContext):
#     lk = api.LiveKitAPI(
#     url=LIVEKIT_URL,
#     api_key=LIVEKIT_API_KEY,
#     api_secret=LIVEKIT_API_SECRET
# )

#     print(f"Job received for room: {ctx.room.name}")
#     res = await lk.room.list_participants(ListParticipantsRequest(
#     room=ctx.room.name
#     ))
#     print(f"Before ctx.connect: \n{res}")
#     await ctx.connect()
#     # REQUIRED — binds worker to room lifecycle

#     res = await lk.room.list_participants(ListParticipantsRequest(
#     room=ctx.room.name
#     ))
#     print(f"After ctx.connect and before agent session: \n{res}")
#     # MCP
#     try:
#         logger.info("🔌 Connecting to MCP server...")
        
#         mcp_server = MCPServerSse(
#             params={"url": N8N_MCP_URL},
#             cache_tools_list=True,
#             name="n8n MCP Server",
#         )
#         async with asyncio.timeout(60):
#             await mcp_server.connect()
#         logger.info(" MCP server connected")
#     except Exception as e:
#         logger.error(f" MCP connection failed: {e}")
#         mcp_server = None


#     # Create agent ONCE
#     if mcp_server:
#         agent = await MCPToolsIntegration.create_agent_with_tools(
#             agent_class=Assistant,
#             mcp_servers=[mcp_server],
#         )
#     else:
#         agent = Assistant()




#     session = AgentSession(
#         stt="assemblyai/universal-streaming:en",
#         llm="openai/gpt-4.1-mini",
#         tts="cartesia/sonic-3:9626c31c-bec5-4cca-baa8-f8ba9e84c8bc",
#         vad=silero.VAD.load(),
#         turn_detection=MultilingualModel(),
#     )
#     # Use THE SAME agent instance
#     await session.start(
#         agent=agent,
#         room=ctx.room,
#     )

#     # Initial greeting
#     await session.generate_reply(
#         instructions="Warmly First Greet the user politely."
#     )


# # -------------------------------------------------------------------
# # WORKER BOOTSTRAP
# # -------------------------------------------------------------------
# if __name__ == "__main__":
#     cli.run_app(
#         WorkerOptions(
#             entrypoint_fnc=entrypoint,
#             worker_type=WorkerType.ROOM,
#             agent_name=AGENT_NAME,
#             ws_url=LIVEKIT_URL,
#             api_key=LIVEKIT_API_KEY,
#             api_secret=LIVEKIT_API_SECRET,
#         )
#     )


from rag.query import get_top_matches
print(get_top_matches("What is the bank address?", 3))