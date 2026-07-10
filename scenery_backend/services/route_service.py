from utils.response import clean_row


def build_route(cursor, route: dict) -> dict:
    route = clean_row(route)
    cursor.execute(
        """
        SELECT s.id, s.name, s.category, s.location, s.recommended_duration, rs.sort_order
        FROM route_spots rs
        JOIN spots s ON rs.spot_id=s.id
        WHERE rs.route_id=%s
        ORDER BY rs.sort_order ASC
        """,
        (route["id"],),
    )
    route["spots"] = cursor.fetchall()
    return route


def save_route_spots(cursor, route_id: int, spot_ids: list[int]):
    cursor.execute("DELETE FROM route_spots WHERE route_id=%s", (route_id,))
    for index, spot_id in enumerate(spot_ids, start=1):
        cursor.execute(
            "INSERT INTO route_spots(route_id, spot_id, sort_order) VALUES(%s,%s,%s)",
            (route_id, spot_id, index),
        )
