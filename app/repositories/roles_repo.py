from sqlalchemy import text


def get_role_ids_by_names(session, role_names: list[str]):
    sql = text("""
        SELECT id, name
        FROM roles
        WHERE name IN :role_names
    """).bindparams(role_names=tuple(role_names))
    return session.execute(sql).mappings().all()


def assign_role_to_user(session, user_id: int, role_id: int):
    sql = text("""
        INSERT IGNORE INTO user_roles (user_id, role_id)
        VALUES (:user_id, :role_id)
    """)
    session.execute(sql, {"user_id": user_id, "role_id": role_id})


def get_user_roles(session, user_id: int):
    sql = text("""
        SELECT r.name
        FROM user_roles ur
        JOIN roles r ON r.id = ur.role_id
        WHERE ur.user_id = :user_id
        ORDER BY r.name
    """)
    rows = session.execute(sql, {"user_id": user_id}).mappings().all()
    return [row["name"] for row in rows]