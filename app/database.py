# -*- coding: utf-8 -*-
"""SQLite 数据库：初始化与连接。"""
import json
import os
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
    if "nickname" not in [r[1] for r in conn.execute("PRAGMA table_info(claim_codes)")]:
        conn.execute("ALTER TABLE claim_codes ADD COLUMN nickname TEXT")
    conn.commit()
    # 空库时自动从种子文件导入（防数据丢失/新部署空库）
    n = conn.execute("SELECT COUNT(*) FROM animals").fetchone()[0]
    if n == 0:
        seed_path = os.path.join(config.DATA_DIR, "animals_seed.json")
        if os.path.exists(seed_path):
            try:
                with open(seed_path, encoding="utf-8") as f:
                    seed = json.load(f)
                animals = seed.get("animals") or []
                codes = seed.get("codes") or []
                tracks = seed.get("tracks") or {}
                conn.executemany(
                    "INSERT OR REPLACE INTO animals VALUES (?,?,?,?,?,?,?,?,?)",
                    [(a.get("id"), a.get("name", ""), a.get("species", ""),
                      a.get("story", ""), a.get("origin", "example"),
                      a.get("data_note", ""),
                      json.dumps(a.get("photo_urls") or [], ensure_ascii=False),
                      a.get("region_label", ""), a.get("created_at")) for a in animals],
                )
                conn.executemany(
                    "INSERT OR REPLACE INTO claim_codes VALUES (?,?,?,?,?)",
                    [list(c) + [None] * (5 - len(c)) for c in codes],
                )
                for aid, pts in tracks.items():
                    conn.executemany(
                        "INSERT OR REPLACE INTO track_points VALUES (?,?,?,?,?)",
                        [(aid, p[0], float(p[1]), float(p[2]), 0.0) for p in pts],
                    )
                conn.commit()
                print(f"[seed] 空库自动导入: {len(animals)}动物/{len(codes)}码/{sum(len(v) for v in tracks.values())}点")
            except Exception as e:
                print(f"[seed] 导入失败: {e}")
    conn.close()


def reset_db():
    """清空全部数据（谨慎使用）。"""
    conn = get_conn()
    for t in ("track_points", "claim_codes", "animals"):
        conn.execute(f"DROP TABLE IF EXISTS {t}")
    conn.commit()
    conn.close()
    init_db()
