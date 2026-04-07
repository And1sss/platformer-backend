
-- 2D Platformer Game Support System
-- db/schema.sql
-- MySQL 8.0+


CREATE DATABASE IF NOT EXISTS platformer_support_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

USE platformer_support_db;


-- roles

CREATE TABLE IF NOT EXISTS roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(32) NOT NULL UNIQUE
) ENGINE=InnoDB;


-- users

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    nickname VARCHAR(64) NOT NULL,
    created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    last_login_at DATETIME(3) NULL,
    is_banned TINYINT(1) NOT NULL DEFAULT 0,
    INDEX idx_users_email (email),
    INDEX idx_users_nickname (nickname),
    INDEX idx_users_banned (is_banned)
) ENGINE=InnoDB;


-- user_roles

CREATE TABLE IF NOT EXISTS user_roles (
    user_id INT NOT NULL,
    role_id INT NOT NULL,
    assigned_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    PRIMARY KEY (user_id, role_id),
    CONSTRAINT fk_user_roles_user
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_user_roles_role
        FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE RESTRICT,
    INDEX idx_user_roles_role_id (role_id)
) ENGINE=InnoDB;


-- game_sessions

CREATE TABLE IF NOT EXISTS game_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    client_platform ENUM('unity','web','mobile') NOT NULL,
    client_version VARCHAR(32) NULL,
    ip VARCHAR(45) NULL,
    started_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    ended_at DATETIME(3) NULL,
    CONSTRAINT fk_game_sessions_user
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_sessions_user_started (user_id, started_at),
    INDEX idx_sessions_platform (client_platform)
) ENGINE=InnoDB;


-- game_events

CREATE TABLE IF NOT EXISTS game_events (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    session_id INT NULL,
    event_type VARCHAR(64) NOT NULL,
    payload_json JSON NOT NULL,
    created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    CONSTRAINT fk_game_events_user
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_game_events_session
        FOREIGN KEY (session_id) REFERENCES game_sessions(id) ON DELETE SET NULL,
    INDEX idx_events_user_time (user_id, created_at),
    INDEX idx_events_type_time (event_type, created_at)
) ENGINE=InnoDB;


-- player_progress

CREATE TABLE IF NOT EXISTS player_progress (
    user_id INT PRIMARY KEY,
    level INT NOT NULL DEFAULT 1,
    xp INT NOT NULL DEFAULT 0,
    soft_currency INT NOT NULL DEFAULT 0,
    hard_currency INT NOT NULL DEFAULT 0,
    updated_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
    CONSTRAINT fk_player_progress_user
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT chk_progress_level CHECK (level >= 1),
    CONSTRAINT chk_progress_xp CHECK (xp >= 0),
    CONSTRAINT chk_progress_soft CHECK (soft_currency >= 0),
    CONSTRAINT chk_progress_hard CHECK (hard_currency >= 0)
) ENGINE=InnoDB;


-- statistics_daily

CREATE TABLE IF NOT EXISTS statistics_daily (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    day DATE NOT NULL,
    sessions_count INT NOT NULL DEFAULT 0,
    events_count INT NOT NULL DEFAULT 0,
    playtime_seconds INT NOT NULL DEFAULT 0,
    wins INT NOT NULL DEFAULT 0,
    losses INT NOT NULL DEFAULT 0,
    score_sum INT NOT NULL DEFAULT 0,
    CONSTRAINT fk_statistics_daily_user
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY uq_statistics_daily_user_day (user_id, day),
    INDEX idx_statistics_day (day),
    INDEX idx_statistics_user_day (user_id, day),
    CONSTRAINT chk_stats_sessions CHECK (sessions_count >= 0),
    CONSTRAINT chk_stats_events CHECK (events_count >= 0),
    CONSTRAINT chk_stats_playtime CHECK (playtime_seconds >= 0),
    CONSTRAINT chk_stats_wins CHECK (wins >= 0),
    CONSTRAINT chk_stats_losses CHECK (losses >= 0),
    CONSTRAINT chk_stats_score_sum CHECK (score_sum >= 0)
) ENGINE=InnoDB;


-- leaderboard_scores

CREATE TABLE IF NOT EXISTS leaderboard_scores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    board_code VARCHAR(64) NOT NULL,
    season INT NOT NULL DEFAULT 1,
    score INT NOT NULL DEFAULT 0,
    updated_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
    CONSTRAINT fk_leaderboard_scores_user
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY uq_leaderboard_user_board_season (user_id, board_code, season),
    INDEX idx_leaderboard_board_season_score (board_code, season, score),
    INDEX idx_leaderboard_user (user_id),
    CONSTRAINT chk_leaderboard_season CHECK (season >= 1),
    CONSTRAINT chk_leaderboard_score CHECK (score >= 0)
) ENGINE=InnoDB;