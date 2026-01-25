import json
import uuid
import datetime
from fastapi import APIRouter, Query

from livekit.api import (
    AccessToken,
    VideoGrants,
    RoomConfiguration,
    RoomAgentDispatch,
)


import os
from dotenv import load_dotenv

load_dotenv()

LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")
LIVEKIT_URL = os.getenv("LIVEKIT_URL")

AGENT_NAME = "lk_agent"

router = APIRouter(prefix="/token", tags=["token"])
@router.get("")
def get_token(identity: str = Query("web-user")):
    room = f"{AGENT_NAME}-{uuid.uuid4().hex[:8]}"

    token = (
        AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET)
        .with_identity(identity)
        .with_name(identity)
        .with_ttl(datetime.timedelta(minutes=10))
        .with_grants(
            VideoGrants(
                room_join=True,
                room=room,
                room_create=True,
            )
        )
        .with_room_config(
            RoomConfiguration(
                agents=[
                    RoomAgentDispatch(
                        agent_name=f"{AGENT_NAME}",
                        metadata=json.dumps({"source": "web"}),
                    )
                ]
            )
        )
    )

    return {
        "url": LIVEKIT_URL,
        "token": token.to_jwt(),
        "room": room,
    }
