from core.config import DB_NAME
from db.connection import get_conn
from db.seed import seed_data


def init_database():
    conn = get_conn(use_db=False)
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
        conn.commit()
    finally:
        conn.close()

    conn = get_conn()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    username VARCHAR(30) NOT NULL UNIQUE,
                    phone VARCHAR(11) NOT NULL UNIQUE,
                    password_hash VARCHAR(255) NOT NULL,
                    role ENUM('tourist', 'admin') NOT NULL DEFAULT 'tourist',
                    status ENUM('active', 'disabled') NOT NULL DEFAULT 'active',
                    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    last_login DATETIME NULL,
                    INDEX idx_users_role(role),
                    INDEX idx_users_status(status)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS spots (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(100) NOT NULL UNIQUE,
                    category VARCHAR(50) NULL,
                    description TEXT NULL,
                    open_time VARCHAR(100) NULL,
                    location VARCHAR(100) NULL,
                    ticket_price DECIMAL(10,2) NOT NULL DEFAULT 0.00,
                    recommended_duration VARCHAR(50) NULL,
                    image_url VARCHAR(255) NULL,
                    created_by INT NULL,
                    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    CONSTRAINT chk_spots_price CHECK (ticket_price >= 0),
                    CONSTRAINT fk_spots_created_by FOREIGN KEY(created_by) REFERENCES users(id) ON DELETE SET NULL,
                    INDEX idx_spots_category(category)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS routes (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(100) NOT NULL UNIQUE,
                    description TEXT NULL,
                    difficulty ENUM('easy', 'medium', 'hard') NOT NULL DEFAULT 'easy',
                    duration_hours DECIMAL(4,1) NOT NULL DEFAULT 1.0,
                    created_by INT NULL,
                    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    CONSTRAINT chk_routes_duration CHECK (duration_hours >= 0),
                    CONSTRAINT fk_routes_created_by FOREIGN KEY(created_by) REFERENCES users(id) ON DELETE SET NULL,
                    INDEX idx_routes_difficulty(difficulty)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS route_spots (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    route_id INT NOT NULL,
                    spot_id INT NOT NULL,
                    sort_order INT NOT NULL DEFAULT 0,
                    UNIQUE KEY uk_route_spot(route_id, spot_id),
                    CONSTRAINT fk_route_spots_route FOREIGN KEY(route_id) REFERENCES routes(id) ON DELETE CASCADE,
                    CONSTRAINT fk_route_spots_spot FOREIGN KEY(spot_id) REFERENCES spots(id) ON DELETE CASCADE,
                    INDEX idx_route_spots_route(route_id),
                    INDEX idx_route_spots_spot(spot_id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS favorites (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    user_id INT NOT NULL,
                    spot_id INT NOT NULL,
                    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE KEY uk_user_spot(user_id, spot_id),
                    CONSTRAINT fk_favorites_user FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
                    CONSTRAINT fk_favorites_spot FOREIGN KEY(spot_id) REFERENCES spots(id) ON DELETE CASCADE,
                    INDEX idx_favorites_user(user_id),
                    INDEX idx_favorites_spot(spot_id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS feedbacks (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    user_id INT NOT NULL,
                    type VARCHAR(50) NOT NULL,
                    rating INT NOT NULL,
                    content TEXT NOT NULL,
                    status ENUM('pending', 'processed', 'ignored') NOT NULL DEFAULT 'pending',
                    reply TEXT NULL,
                    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    processed_at DATETIME NULL,
                    CONSTRAINT chk_feedback_rating CHECK (rating BETWEEN 1 AND 5),
                    CONSTRAINT fk_feedbacks_user FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
                    INDEX idx_feedback_user(user_id),
                    INDEX idx_feedback_type(type),
                    INDEX idx_feedback_status(status),
                    INDEX idx_feedback_rating(rating)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS faqs (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    question VARCHAR(255) NOT NULL,
                    answer TEXT NOT NULL,
                    category VARCHAR(50) NULL,
                    keywords VARCHAR(255) NULL,
                    sort_order INT NOT NULL DEFAULT 0,
                    created_by INT NULL,
                    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    CONSTRAINT fk_faqs_created_by FOREIGN KEY(created_by) REFERENCES users(id) ON DELETE SET NULL,
                    INDEX idx_faq_category(category)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS chat_records (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    session_id VARCHAR(64) NOT NULL,
                    user_id INT NOT NULL,
                    role ENUM('user', 'assistant') NOT NULL,
                    content TEXT NOT NULL,
                    source ENUM('user', 'faq', 'deepseek', 'fallback') NOT NULL DEFAULT 'user',
                    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    CONSTRAINT fk_chat_user FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
                    INDEX idx_chat_user_session(user_id, session_id, created_at),
                    INDEX idx_chat_source(source)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """
            )
            for table, index_name in (
                ("spots", "idx_spots_status"),
                ("routes", "idx_routes_status"),
                ("faqs", "idx_faq_status"),
            ):
                cursor.execute(
                    """
                    SELECT COUNT(*) AS total
                    FROM information_schema.statistics
                    WHERE table_schema=%s AND table_name=%s AND index_name=%s
                    """,
                    (DB_NAME, table, index_name),
                )
                if cursor.fetchone()["total"]:
                    cursor.execute(f"ALTER TABLE {table} DROP INDEX {index_name}")
            for table in ("spots", "routes", "faqs"):
                cursor.execute(
                    """
                    SELECT COUNT(*) AS total
                    FROM information_schema.columns
                    WHERE table_schema=%s AND table_name=%s AND column_name='status'
                    """,
                    (DB_NAME, table),
                )
                if cursor.fetchone()["total"]:
                    cursor.execute(f"ALTER TABLE {table} DROP COLUMN status")
            seed_data(cursor)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
