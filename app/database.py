# -*- coding: utf-8 -*-
"""SQLite 数据库：初始化与连接。"""
import json
import sqlite3

import config

SCHEMA = """
CREATE TABLE IF NOT EXISTS animals (
    id           TEXT PRIMARY KEY,
    name         TEXT NOT NULL,
    species      TEXT NOT NULL,
    story        TEXT NOT NULL,
    origin       TEXT DEFAULT 'example',
    data_note    TEXT DEFAULT '',
    photo_urls   TEXT DEFAULT '[]',
    region_label TEXT DEFAULT '',
    created_at   TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS claim_codes (
    code       TEXT PRIMARY KEY,
    animal_id  TEXT NOT NULL,
    status     TEXT DEFAULT 'unused',
    claimed_at TEXT,
    FOREIGN KEY (animal_id) REFERENCES animals(id)
);

CREATE TABLE IF NOT EXISTS track_points (
    animal_id TEXT NOT NULL,
    ts        TEXT NOT NULL,
    lat       REAL NOT NULL,
    lon       REAL NOT NULL,
    alt       REAL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_track_animal ON track_points(animal_id);
"""


def get_conn(db_path=None):
    conn = sqlite3.connect(db_path or config.DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    conn.executescript(SCHEMA)
    # 兼容旧库：补齐新增列
    cols = [r[1] for r in conn.execute("PRAGMA table_info(animals)")]
    if "region_label" not in cols:
        conn.execute("ALTER TABLE animals ADD COLUMN region_label TEXT DEFAULT ''")
    conn.commit()
    conn.close()


def reset_db():
    """清空全部数据（谨慎使用）。"""
    conn = get_conn()
    for t in ("track_points", "claim_codes", "animals"):
        conn.execute(f"DROP TABLE IF EXISTS {t}")
    conn.commit()
    conn.close()
    init_db()
