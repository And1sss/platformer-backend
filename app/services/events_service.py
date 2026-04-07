import json

from app.extensions import db
from app.repositories.events_repo import insert_game_event


def post_event_service(user_id: int, payload: dict) -> dict:
    user_id = int(user_id)

    session_id = payload.get("sessionId")
    event_type = payload["eventType"]
    event_payload = payload["payload"]

    payload_json = json.dumps(event_payload, ensure_ascii=False)

    insert_game_event(
        db.session,
        user_id=user_id,
        session_id=session_id,
        event_type=event_type,
        payload_json=payload_json
    )

    db.session.commit()

    return {
        "accepted": True
    }