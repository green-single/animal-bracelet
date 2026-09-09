# -*- coding: utf-8 -*-
"""
OBIS 真实数据同步模块
=====================
数据"时时流动"的核心：系统可以按需从 OBIS（公开海洋生物数据库，
无需注册）在线拉取真实遥测记录，合并进本地轨迹，实现数据自动更新。

对外函数：
  import_from_raw(animal_id, raw_path)  从本地已拉取的 OBIS 原始 JSON 导入
  sync_animal(animal_id, datasetid, pages=20)  在线增量同步（拉取最新记录并合并）
"""
import datetime
import json
import os
import sys
import time
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import init_db, get_conn  # noqa: E402

API = "https://api.obis.org/v3/occurrence"
UA = "animal-bracelet/1.0 (personal DIY project)"


def _get(params, retries=3):
    url = API + "?" + urllib.parse.urlencode(params)
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.load(r)
        except Exception:
            if i == retries - 1:
                raise
            time.sleep(2)


def _norm_ts(s):
    if not s:
        return None
    return s.replace("T", " ").replace("Z", "").replace("+00:00", "")[:19]


def _parse_records(recs):
    pts = []
    for r in recs:
        lon, lat = r.get("decimalLongitude"), r.get("decimalLatitude")
        ts = _norm_ts(r.get("eventDate"))
        if lon is None or lat is None or not ts:
            continue
        try:
            lat, lon = float(lat), float(lon)
        except (TypeError, ValueError):
            continue
        pts.append((ts, lat, lon))
    pts.sort(key=lambda x: x[0])
    return pts


def _merge_and_store(animal_id, new_pts, note, region_label=None, max_points=600):
    """把新点合并进数据库（按时间去重），并更新动物的数据说明。"""
    init_db()
    conn = get_conn()
    cur = conn.cursor()
    existing = {
        r["ts"] for r in cur.execute(
            "SELECT ts FROM track_points WHERE animal_id=?", (animal_id,)
        ).fetchall()
    }
    added = 0
    rows = []
    for ts, lat, lon in new_pts:
        if ts in existing:
            continue
        existing.add(ts)
        rows.append((animal_id, ts, lat, lon, 0))
        added += 1
    if rows:
        cur.executemany(
            "INSERT INTO track_points (animal_id, ts, lat, lon, alt) VALUES (?,?,?,?,?)", rows
        )
    # 上限裁剪：保留时间上最新的 max_points 个点
    cur.execute(
        "DELETE FROM track_points WHERE animal_id=? AND ts NOT IN "
        "(SELECT ts FROM track_points WHERE animal_id=? ORDER BY ts DESC LIMIT ?)",
        (animal_id, animal_id, max_points),
    )
    cur.execute(
        "UPDATE animals SET data_note=?, origin='obis', region_label=COALESCE(?, region_label) "
        "WHERE id=?",
        (note, region_label, animal_id),
    )
    conn.commit()
    total = cur.execute("SELECT COUNT(*) FROM track_points WHERE animal_id=?", (animal_id,)).fetchone()[0]
    conn.close()
    return {"added": added, "total": total}


def import_from_raw(animal_id, raw_path, note=None, region_label=None, max_points=300):
    """从本地 OBIS 原始 JSON 导入（全量，适合首次接入）。"""
    with open(raw_path, encoding="utf-8") as f:
        recs = json.load(f)
    pts = _parse_records(recs)
    n = min(len(pts), max_points)
    if n < 2:
        return {"added": 0, "total": 0, "error": "有效点不足"}
    idx = [round(i * (len(pts) - 1) / (n - 1)) for i in range(n)]
    chosen = [pts[i] for i in idx]
    note = note or (
        "真实遥测数据 · 来源 OBIS 公开数据库（澳大利亚东海岸绿海龟卫星追踪 2010–2011，"
        "个体 Noel），研究机构公开发布，CC 协议；定位经均匀抽样，系统可持续同步更新。"
    )
    init_db()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM track_points WHERE animal_id=?", (animal_id,))
    cur.executemany(
        "INSERT INTO track_points (animal_id, ts, lat, lon, alt) VALUES (?,?,?,?,0)",
        [(animal_id, ts, la, lo) for ts, la, lo in chosen],
    )
    cur.execute(
        "UPDATE animals SET name='Noel', species='绿海龟', "
        "origin='obis', data_note=?, region_label=COALESCE(?, region_label) WHERE id=?",
        (note, region_label, animal_id),
    )
    conn.commit()
    conn.close()
    return {"added": n, "total": n, "first": chosen[0], "last": chosen[-1]}


def sync_animal(animal_id, datasetid, pages=20, note=None):
    """在线增量同步：从 OBIS 拉取该数据集最新记录（每页 10 条）合并进轨迹。"""
    recs = []
    for off in range(0, pages * 10, 10):
        try:
            d = _get({"datasetid": datasetid, "limit": 10, "offset": off})
        except Exception:
            break
        recs.extend(d.get("results", []))
        if len(d.get("results", [])) < 10:
            break
        time.sleep(0.2)
    pts = _parse_records(recs)
    if not pts:
        return {"added": 0, "total": 0, "error": "OBIS 未返回有效记录"}
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    note = note or (
        f"真实遥测数据 · 来源 OBIS 公开数据库（{datasetid[:8]}…），"
        f"最近同步 {now}，数据持续自动更新。"
    )
    return _merge_and_store(animal_id, pts, note)
