# -*- coding: utf-8 -*-
"""
通用 Movebank 数据同步脚本
支持同步多个动物：Noé 白鹳 + Lumi 欧斑鸠
用法：python sync_movebank_all.py
"""
import subprocess
import csv
import io
import json
import sqlite3
import os
import math
from datetime import datetime

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
MB_AUTH = (os.environ.get("MB_USER", "green"), os.environ.get("MB_PASS", "Water1221"))
CURL_BIN = "curl.exe" if os.name == "nt" else "curl"
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "animals.db")

# 需要同步的动物列表
ANIMALS = [
    {
        "animal_id": "noe",
        "name": "Noé",
        "species": "White Stork (Ciconia ciconia)",
        "study_id": "1562253659",  # LifeTrack White Stork Sarralbe (CC0)
        "individual_id": "1600899302",  # Noé
        "license": "CC0",
        "study_name": "LifeTrack White Stork Sarralbe",
    },
    {
        "animal_id": "turtle",
        "name": "Lumi",
        "species": "European Turtle Dove (Streptopelia turtur)",
        "study_id": "3413045568",  # Habitrack European Turtle Dove (CC_BY)
        "individual_id": "7625503924",  # CZP_HN5211 (Lumi)
        "license": "CC_BY",
        "study_name": "Habitrack European Turtle Dove",
    },
    {
        "animal_id": "redkite",
        "name": "Athos",
        "species": "Red Kite (Milvus milvus)",
        "study_id": "501903109",  # Red Kite MPI-AB Baden-Wuerttemberg (CC0)
        "individual_id": "864946973",  # Athos 180806 (JC50494)
        "license": "CC0",
        "study_name": "Red Kite MPI-AB Baden-Wuerttemberg",
    },
    {
        "animal_id": "honeybuzzard",
        "name": "Mel",
        "species": "European Honey Buzzard (Pernis apivorus)",
        "study_id": "186178781",  # Raptors NABU Moessingen (CC_BY)
        "individual_id": "2842545544",  # Honey Buzzard 12212 (DER KT2169)
        "license": "CC_BY",
        "study_name": "Raptors NABU Moessingen",
    },
    {
        "animal_id": "herringgull",
        "name": "Silver",
        "species": "Herring Gull (Larus argentatus)",
        "study_id": "1258895879",  # Herring Gull DELTATRACK (CC0)
        "individual_id": "1774067789",  # 5417006
        "license": "CC0",
        "study_name": "Herring Gull DELTATRACK",
    },
]


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def fetch_movebank_data(study_id, individual_id):
    """从 Movebank 下载单个个体的完整数据"""
    url = (f"https://www.movebank.org/movebank/service/direct-read?"
           f"entity_type=event&study_id={study_id}"
           f"&individual_id={individual_id}&max_events=200000")
    r = subprocess.run(
        [CURL_BIN, "-s", "-A", UA, "-u", f"{MB_AUTH[0]}:{MB_AUTH[1]}",
         "-L", "--max-time", "120", url],
        capture_output=True, text=True, timeout=125
    )
    if not r.stdout or 'timestamp' not in r.stdout[:500]:
        raise Exception(f"Movebank 返回无效数据: {r.stdout[:200]}")
    reader = csv.DictReader(io.StringIO(r.stdout))
    records = []
    for row in reader:
        try:
            ts = row.get('timestamp', '') or ''
            lat_raw = row.get('location_lat') or ''
            lon_raw = row.get('location_long') or ''
            # 字段可能缺失或为空（部分传感器行），健壮处理
            try:
                lat = float(lat_raw) if lat_raw not in (None, '') else 0.0
                lon = float(lon_raw) if lon_raw not in (None, '') else 0.0
            except (ValueError, TypeError):
                continue
            if ts and lat != 0 and lon != 0 and -90 <= lat <= 90 and -180 <= lon <= 180:
                try:
                    dt = datetime.fromtimestamp(int(ts)/1000, tz=datetime.timezone.utc)
                    ts_formatted = dt.strftime('%Y-%m-%d %H:%M:%S')
                except:
                    ts_formatted = ts[:19].replace('T', ' ')
                records.append({'ts': ts_formatted, 'lat': lat, 'lon': lon})
        except (ValueError, KeyError, TypeError):
            continue
    return records


def daily_downsample(records):
    """按日期降采样，每天保留第一个点"""
    daily = {}
    for r in records:
        day = r['ts'][:10]
        if day not in daily:
            daily[day] = r
    return sorted(daily.values(), key=lambda x: x['ts'])


def calc_total_distance(records):
    """计算累计迁徙距离（km）"""
    total = 0
    for i in range(1, len(records)):
        p1, p2 = records[i-1], records[i]
        R = 6371
        lat1, lat2 = math.radians(p1["lat"]), math.radians(p2["lat"])
        dlat = math.radians(p2["lat"] - p1["lat"])
        dlon = math.radians(p2["lon"] - p1["lon"])
        a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
        c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
        total += R * c
    return total


def update_database(animal_id, name, species, study_name, individual_id, license, records):
    """增量更新数据库"""
    conn = get_db_connection()
    c = conn.cursor()
    
    # 获取已有数据的日期
    c.execute("SELECT ts FROM track_points WHERE animal_id = ?", (animal_id,))
    existing_dates = set(row['ts'][:10] for row in c.fetchall())
    
    # 只插入新的日期
    new_points = [r for r in records if r['ts'][:10] not in existing_dates]
    
    if new_points:
        c.executemany(
            "INSERT OR IGNORE INTO track_points (animal_id, ts, lat, lon, alt) VALUES (?, ?, ?, ?, ?)",
            [(animal_id, r['ts'], r['lat'], r['lon'], 0) for r in new_points]
        )
    
    # 更新动物元数据
    latest_ts = records[-1]['ts'] if records else None
    total_dist = calc_total_distance(records)
    data_note = (f"Movebank {license} | {study_name} | individual_id={individual_id} | "
                 f"自动同步至 {latest_ts} | {len(records)} daily points | {int(total_dist)} km")
    
    c.execute("UPDATE animals SET data_note = ? WHERE id = ?", (data_note, animal_id))
    
    conn.commit()
    
    # 统计
    c.execute("SELECT COUNT(*) as cnt FROM track_points WHERE animal_id = ?", (animal_id,))
    total_count = c.fetchone()['cnt']
    
    conn.close()
    
    return {
        "raw_count": len(records),
        "daily_count": len(records),
        "new_points": len(new_points),
        "total_points": total_count,
        "latest_ts": latest_ts,
        "total_dist": int(total_dist),
    }


def main():
    print("=" * 70)
    print("Movebank 数据自动同步（多动物）")
    print("=" * 70)
    
    results = {}
    
    for animal in ANIMALS:
        animal_id = animal['animal_id']
        name = animal['name']
        print(f"\n{'─' * 70}")
        print(f"同步 {name} ({animal_id})...")
        print(f"  study_id: {animal['study_id']}")
        print(f"  individual_id: {animal['individual_id']}")
        print(f"  license: {animal['license']}")
        
        try:
            # 1. 从 Movebank 下载数据
            print("  正在从 Movebank 拉取数据...")
            raw_records = fetch_movebank_data(animal['study_id'], animal['individual_id'])
            print(f"  ✅ 获取到 {len(raw_records)} 条原始数据")
            
            # 2. 清洗和降采样
            daily_records = daily_downsample(raw_records)
            print(f"  ✅ 降采样后保留 {len(daily_records)} 个每日定位点")
            
            if daily_records:
                print(f"     时间范围: {daily_records[0]['ts']} -> {daily_records[-1]['ts']}")
            
            # 3. 更新数据库
            stats = update_database(
                animal_id, name, animal['species'],
                animal['study_name'], animal['individual_id'],
                animal['license'], daily_records
            )
            
            print(f"  📊 数据库中已有 {stats['total_points']} 天的定位数据")
            print(f"  🆕 新增 {stats['new_points']} 天的定位点")
            print(f"  ✅ 数据更新至 {stats['latest_ts']}，累计迁徙 {stats['total_dist']} km")
            
            results[animal_id] = {"ok": True, **stats}
            
        except Exception as e:
            print(f"  ❌ 同步失败: {e}")
            results[animal_id] = {"ok": False, "error": str(e)}
        
        # 间隔5秒，避免速率限制
        if animal != ANIMALS[-1]:
            print("  等待5秒...")
            import time
            time.sleep(5)
    
    print(f"\n{'=' * 70}")
    print("同步完成！")
    print("=" * 70)
    for animal_id, result in results.items():
        if result.get('ok'):
            print(f"  ✅ {animal_id}: {result['total_points']} 点, 新增 {result['new_points']}, 最新 {result['latest_ts']}")
        else:
            print(f"  ❌ {animal_id}: {result.get('error', '未知错误')}")
    
    return results


if __name__ == "__main__":
    main()
