from core.security import hash_password


OLD_SAMPLE_SPOTS = {"云湖观景台", "古栈道", "民俗文化馆", "亲水步道"}
ZHONGSHANLING_SPOTS = {"中山陵", "音乐台", "流徽榭（水榭）", "行健亭", "光化亭"}

SPOT_DESCRIPTIONS = {
    "中山陵": "中山陵是孙中山先生的陵寝，也是南京钟山风景名胜区最具代表性的核心景点。建筑群依山势层层展开，整体氛围庄严肃穆，游客可以在游览过程中了解近代历史、民国建筑风格和纪念性景区的文化意义。",
    "音乐台": "音乐台位于中山陵广场南侧，是景区内兼具建筑美感与休闲氛围的人文景观。半圆形舞台、弧形回廊和开阔草坪相互映衬，常有白鸽聚集，适合游客短暂停留、拍照和感受中山陵周边的宁静环境。",
    "流徽榭（水榭）": "流徽榭又称水榭，临水而建，周边树木葱郁，环境清幽，是中山陵景区内较有园林意趣的观景节点。游客在游览主景点后，可以在这里休息、观水、拍照，也能感受景区自然景观与纪念建筑之间的过渡。",
    "行健亭": "行健亭位于中山陵景区步行游线附近，亭名取意积极向上、自强不息，具有一定的纪念和文化象征意义。它适合作为路线中的休息点和讲解点，游客可以在此稍作停留，了解景区节点布局与相关文化内涵。",
    "光化亭": "光化亭周边空间较为开阔，绿树环绕，环境安静，是游客进行短暂停留和了解景区历史文化的节点之一。相比核心景点，这里节奏更舒缓，适合安排在深度游路线中，作为补充游览和休息观景的位置。",
}

ROUTE_DESCRIPTIONS = {
    "中山陵轻松游（1-2小时）": "适合时间较少、体力有限或首次到访的游客，重点游览中山陵核心区域，并顺路参观音乐台。路线节点少、节奏轻松，既能看到景区标志性景观，也方便游客快速了解中山陵的整体风貌。",
    "中山陵普通游（2-3小时）": "适合大多数游客，覆盖中山陵、音乐台和流徽榭（水榭）三个主要节点。路线兼顾历史文化、建筑观赏和休闲观景，游览强度适中，适合希望比较完整体验中山陵景区的游客选择。",
    "中山陵深度游（4-5小时）": "适合时间充足、希望深度了解景区的游客，串联中山陵、音乐台、流徽榭（水榭）、行健亭和光化亭。路线覆盖核心景点与周边节点，内容更完整，能够体现景区历史文化、自然环境和游线层次。",
}

DEFAULT_ROUTE_SPOTS = {
    "中山陵轻松游（1-2小时）": ["中山陵", "音乐台"],
    "中山陵普通游（2-3小时）": ["中山陵", "音乐台", "流徽榭（水榭）"],
    "中山陵深度游（4-5小时）": ["中山陵", "音乐台", "流徽榭（水榭）", "行健亭", "光化亭"],
}


def reset_old_sample_data(cursor):
    """如果检测到早期示例景区数据，则清理示例业务数据，重新写入南京中山陵数据。"""
    cursor.execute(
        "SELECT COUNT(*) AS total FROM spots WHERE name IN (%s,%s,%s,%s)",
        tuple(OLD_SAMPLE_SPOTS),
    )
    if cursor.fetchone()["total"] == 0:
        return
    cursor.execute("DELETE FROM chat_records")
    cursor.execute("DELETE FROM feedbacks")
    cursor.execute("DELETE FROM favorites")
    cursor.execute("DELETE FROM route_spots")
    cursor.execute("DELETE FROM routes")
    cursor.execute("DELETE FROM faqs")
    cursor.execute("DELETE FROM spots")


def sync_default_descriptions(cursor):
    for name, description in SPOT_DESCRIPTIONS.items():
        cursor.execute("UPDATE spots SET description=%s WHERE name=%s", (description, name))
    for name, description in ROUTE_DESCRIPTIONS.items():
        cursor.execute("UPDATE routes SET description=%s WHERE name=%s", (description, name))


def sync_default_route_spots(cursor):
    cursor.execute("SELECT id, name FROM spots WHERE name IN (%s,%s,%s,%s,%s)", tuple(ZHONGSHANLING_SPOTS))
    spot_map = {row["name"]: row["id"] for row in cursor.fetchall()}
    cursor.execute(
        "SELECT id, name FROM routes WHERE name IN (%s,%s,%s)",
        tuple(DEFAULT_ROUTE_SPOTS.keys()),
    )
    for route in cursor.fetchall():
        cursor.execute("DELETE FROM route_spots WHERE route_id=%s", (route["id"],))
        for index, spot_name in enumerate(DEFAULT_ROUTE_SPOTS[route["name"]], start=1):
            spot_id = spot_map.get(spot_name)
            if spot_id:
                cursor.execute(
                    "INSERT INTO route_spots(route_id, spot_id, sort_order) VALUES(%s,%s,%s)",
                    (route["id"], spot_id, index),
                )


def seed_data(cursor):
    cursor.execute("SELECT id FROM users WHERE username=%s", ("admin",))
    admin = cursor.fetchone()
    if admin:
        admin_id = admin["id"]
    else:
        cursor.execute(
            "INSERT INTO users(username, phone, password_hash, role) VALUES(%s,%s,%s,'admin')",
            ("admin", "13800000000", hash_password("Admin123456")),
        )
        admin_id = cursor.lastrowid

    reset_old_sample_data(cursor)

    cursor.execute("SELECT COUNT(*) AS total FROM spots")
    if cursor.fetchone()["total"] == 0:
        spots = [
            (
                "中山陵",
                "核心景点",
                SPOT_DESCRIPTIONS["中山陵"],
                "08:30-17:00",
                "南京市玄武区石象路7号钟山风景区内",
                0,
                "60-90分钟",
            ),
            (
                "音乐台",
                "人文景观",
                SPOT_DESCRIPTIONS["音乐台"],
                "07:00-18:00",
                "中山陵广场南侧",
                10,
                "30-40分钟",
            ),
            (
                "流徽榭（水榭）",
                "园林景观",
                SPOT_DESCRIPTIONS["流徽榭（水榭）"],
                "全天开放",
                "中山陵景区水域附近",
                0,
                "20-30分钟",
            ),
            (
                "行健亭",
                "纪念建筑",
                SPOT_DESCRIPTIONS["行健亭"],
                "全天开放",
                "中山陵景区步行游线旁",
                0,
                "15-20分钟",
            ),
            (
                "光化亭",
                "纪念建筑",
                SPOT_DESCRIPTIONS["光化亭"],
                "全天开放",
                "中山陵景区周边游线",
                0,
                "15-20分钟",
            ),
        ]
        for item in spots:
            cursor.execute(
                """
                INSERT INTO spots(name, category, description, open_time, location, ticket_price, recommended_duration, created_by)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
                """,
                (*item, admin_id),
            )

    cursor.execute("SELECT COUNT(*) AS total FROM routes")
    if cursor.fetchone()["total"] == 0:
        cursor.execute("SELECT id, name FROM spots ORDER BY id ASC")
        spot_map = {row["name"]: row["id"] for row in cursor.fetchall()}
        route_defs = [
            (
                "中山陵轻松游（1-2小时）",
                ROUTE_DESCRIPTIONS["中山陵轻松游（1-2小时）"],
                "easy",
                1.5,
                DEFAULT_ROUTE_SPOTS["中山陵轻松游（1-2小时）"],
            ),
            (
                "中山陵普通游（2-3小时）",
                ROUTE_DESCRIPTIONS["中山陵普通游（2-3小时）"],
                "medium",
                2.5,
                DEFAULT_ROUTE_SPOTS["中山陵普通游（2-3小时）"],
            ),
            (
                "中山陵深度游（4-5小时）",
                ROUTE_DESCRIPTIONS["中山陵深度游（4-5小时）"],
                "hard",
                4.5,
                DEFAULT_ROUTE_SPOTS["中山陵深度游（4-5小时）"],
            ),
        ]
        for name, desc, difficulty, hours, spot_names in route_defs:
            cursor.execute(
                "INSERT INTO routes(name, description, difficulty, duration_hours, created_by) VALUES(%s,%s,%s,%s,%s)",
                (name, desc, difficulty, hours, admin_id),
            )
            route_id = cursor.lastrowid
            ids = [spot_map[name] for name in spot_names if name in spot_map]
            for index, spot_id in enumerate(ids, start=1):
                cursor.execute(
                    "INSERT INTO route_spots(route_id, spot_id, sort_order) VALUES(%s,%s,%s)",
                    (route_id, spot_id, index),
                )

    cursor.execute("SELECT COUNT(*) AS total FROM faqs")
    if cursor.fetchone()["total"] == 0:
        faqs = [
            ("中山陵开放时间是什么？", "中山陵景区通常白天开放，核心区域开放时间一般可参考08:30-17:00，具体以景区当天公告为准。建议出行前关注官方信息。", "开放时间", "中山陵,开放时间,几点,营业"),
            ("中山陵需要预约吗？", "中山陵属于热门景区，节假日和旅游高峰期建议提前关注官方预约要求，按规定预约或错峰出行。", "预约", "中山陵,预约,预约参观,节假日"),
            ("中山陵门票多少钱？", "中山陵陵寝主体区域通常免费开放，音乐台等周边景点可能单独收费，具体票价以景区公告为准。", "门票", "中山陵,门票,价格,免费,音乐台"),
            ("中山陵适合游览多久？", "如果只游览中山陵核心区域，约1-2小时；若加入音乐台和流徽榭（水榭），约2-3小时；深度游览周边节点建议预留4-5小时。", "游览时长", "中山陵,游览多久,时长,路线"),
            ("怎么去中山陵？", "游客可乘坐公共交通到达钟山风景区附近，再步行或换乘景区交通前往中山陵。自驾游客需提前关注停车和交通管制信息。", "交通", "中山陵,怎么去,交通,公交,自驾"),
            ("音乐台有什么特色？", "音乐台位于中山陵广场南侧，建筑造型优雅，常有白鸽聚集，是游客休憩、拍照和感受景区氛围的热门地点。", "景点介绍", "音乐台,白鸽,特色,拍照"),
            ("流徽榭（水榭）在哪里？", "流徽榭（水榭）位于中山陵景区游览范围内，临水而建，环境清幽，适合在游览途中休息和观景。", "景点介绍", "流徽榭,水榭,位置,在哪里"),
            ("游览中山陵有哪些注意事项？", "中山陵为纪念性景区，游览时应保持安静有序，爱护环境，不攀爬建筑，不乱扔垃圾，并根据台阶较多的特点合理安排体力。", "游览须知", "中山陵,注意事项,参观礼仪,台阶"),
            ("推荐哪条中山陵路线？", "时间较少可选择1-2小时轻松游；普通游客推荐2-3小时普通游；时间充足且希望完整体验景区文化的游客可选择4-5小时深度游。", "路线推荐", "中山陵,路线推荐,轻松游,普通游,深度游"),
            ("如何在系统中收藏景点或提交反馈？", "登录游客账号后，可在景点列表点击收藏景点；也可以进入游客反馈页面填写反馈类型、评分和内容，提交后可在我的反馈中查看处理状态。", "系统使用", "收藏,反馈,系统使用,我的收藏,我的反馈"),
        ]
        for q, a, c, k in faqs:
            cursor.execute(
                "INSERT INTO faqs(question, answer, category, keywords, created_by) VALUES(%s,%s,%s,%s,%s)",
                (q, a, c, k, admin_id),
            )

    sync_default_descriptions(cursor)
    sync_default_route_spots(cursor)
