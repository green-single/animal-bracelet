# -*- coding: utf-8 -*-
"""
Movebank 数据自动同步脚本
从 Movebank 拉取 Noé 白鹳的最新数据，增量更新到数据库
用法：python scripts/sync_movebank.py
"""
import os
import sys
import csv
import io
import json
import sqlite3
import subprocess
import math
from datetime import datetime

# Movebank 配置
MOVEBANK_USER = "green"
MOVEBANK_PASS = "Water1221"
STUDY_ID = "1562253659"  # LifeTrack White Stork Sarralbe (CC0)
INDIVIDUAL_ID = "1600899302"  # Noé
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# 数据库路径
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "animals.db")


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def fetch_movebank_data():
    """从 Movebank API 拉取 Noé 的所有 GPS 数据（CSV格式）"""
    url = ("https://www.movebank.org/movebank/service/direct-read?entity_type=event"
           "&study_id=%s&individual_id=%s&max_events=200000" % (STUDY_ID, INDIVIDUAL_ID))
    
    print(f"正在从 Movebank 拉取数据...")
    r = subprocess.run(
        ["curl.exe", "-s", "-A", UA, "-u", "%s:%s" % (MOVEBANK_USER, MOVEBANK_PASS),
         "-L", "--max-time", "120", url],
        capture_output=True, text=True, timeout=125
    )
    out = r.stdout
    
    if not out or "timestamp" not in out[:300]:
        print(f"❌ 拉取失败，返回内容前300字符: {out[:300]}")
        return []
    
    # 解析 CSV
    reader = csv.DictReader(io.StringIO(out))
    rows = list(reader)
    print(f"✅ 从 Movebank 获取到 {len(rows)} 条原始数据")
    
    # 清洗数据
    valid = []
    for row in rows:
        try:
            ts = row.get("timestamp", "").strip()
            lat = float(row.get("location_lat", 0))
            lon = float(row.get("location_long", 0))
            alt = float(row.get("height_above_ellipsoid", 0) or 0)
            if ts and lat != 0 and lon != 0 and -90 <= lat <= 90 and -180 <= lon <= 180:
                # 转换时间格式: Movebank timestamp 是毫秒时间戳
                try:
                    dt = datetime.utcfromtimestamp(int(ts) / 1000)
                    ts_formatted = dt.strftime("%Y-%m-%d %H:%M:%S")
                except (ValueError, OSError):
                    # 可能已经是日期格式
                    ts_formatted = ts[:19].replace("T", " ")
                valid.append({"ts": ts_formatted, "lat": lat, "lon": lon, "alt": alt})
        except (ValueError, KeyError):
            continue
    
    valid.sort(key=lambda x: x["ts"])
    print(f"✅ 清洗后有效数据: {len(valid)} 条")
    if valid:
        print(f"   时间范围: {valid[0]['ts']} -> {valid[-1]['ts']}")
    return valid


def daily_downsample(records):
    """降采样：每天保留第一个点"""
    if not records:
        return []
    daily = {}
    for r in records:
        day = r["ts"][:10]
        if day not in daily:
            daily[day] = r
    result = sorted(daily.values(), key=lambda x: x["ts"])
    print(f"✅ 降采样后保留 {len(result)} 个每日定位点")
    return result


def calc_total_distance(records):
    """计算累计迁徙距离（Haversine）"""
    if len(records) < 2:
        return 0
    total = 0
    R = 6371
    for i in range(1, len(records)):
        p1, p2 = records[i-1], records[i]
        lat1, lat2 = math.radians(p1["lat"]), math.radians(p2["lat"])
        dlat = math.radians(p2["lat"] - p1["lat"])
        dlon = math.radians(p2["lon"] - p1["lon"])
        a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        total += R * c
    return total


def update_database(records, animal_id="noe"):
    """增量更新数据库：只添加新的定位点"""
    conn = get_db_connection()
    
    # 获取数据库中已有的日期（按日期去重，避免时间戳细微差别导致重复）
    existing = conn.execute(
        "SELECT ts FROM track_points WHERE animal_id = ?", (animal_id,)
    ).fetchall()
    existing_dates = set(r["ts"][:10] for r in existing)  # YYYY-MM-DD
    print(f"📊 数据库中已有 {len(existing_dates)} 天的定位数据")
    
    # 只添加新日期的点
    new_points = [r for r in records if r["ts"][:10] not in existing_dates]
    print(f"🆕 新增 {len(new_points)} 天的定位点")
    
    if new_points:
        conn.executemany(
            "INSERT OR IGNORE INTO track_points (animal_id, ts, lat, lon, alt) VALUES (?, ?, ?, ?, ?)",
            [(animal_id, r["ts"], r["lat"], r["lon"], r["alt"]) for r in new_points]
        )
        conn.commit()
    
    # 更新动物的 data_note
    if records:
        latest_ts = records[-1]["ts"]
        total_dist = calc_total_distance(records)
        conn.execute(
            "UPDATE animals SET data_note = ? WHERE id = ?",
            (f"Movebank CC0 | LifeTrack White Stork Sarralbe | individual_id={INDIVIDUAL_ID} | 自动同步至 {latest_ts} | {len(records)} daily points | {int(total_dist)} km", animal_id)
        )
        conn.commit()
        print(f"✅ 数据更新至 {latest_ts}，累计迁徙 {int(total_dist)} km")
    
    # 统计总数
    total = conn.execute(
        "SELECT COUNT(*) as cnt FROM track_points WHERE animal_id = ?", (animal_id,)
    ).fetchone()["cnt"]
    
    conn.close()
    print(f"📈 数据库中 Noé 共有 {total} 个定位点")
    return len(new_points)


def main():
    print("=" * 60)
    print("Movebank 数据自动同步 - Noé 白鹳")
    print("=" * 60)
    
    # 1. 拉取数据
    raw_records = fetch_movebank_data()
    if not raw_records:
        print("❌ 未获取到数据，同步终止")
        sys.exit(1)
    
    # 2. 降采样
    daily_records = daily_downsample(raw_records)
    
    # 3. 更新数据库
    new_count = update_database(daily_records)
    
    print("=" * 60)
    if new_count > 0:
        print(f"✅ 同步完成！新增 {new_count} 个定位点")
    else:
        print("✅ 同步完成！数据已是最新，没有新增")
    print("=" * 60)


if __name__ == "__main__":
    main()
