from sqlalchemy import text


def insert_game_event(session, user_id: int, session_id, event_type: str, payload_json: str):
    sql = text("""
        INSERT INTO game_events (user_id, session_id, event_type, payload_json)
        VALUES (:user_id, :session_id, :event_type, CAST(:payload_json AS JSON))
    """)
    session.execute(sql, {
        "user_id": user_id,
        "session_id": session_id,
        "event_type": event_type,
        "payload_json": payload_json
    })