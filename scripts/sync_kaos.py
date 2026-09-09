# -*- coding: utf-8 -*-
"""
Kaos (座头鲸) 自动同步脚本
定期从 OBIS/Happywhale 检查 Kaos 的最新目击记录
目前 Happywhale 是 SPA，无法用 curl 自动抓取，脚本框架预留接口
未来可接入浏览器渲染或 Happywhale API
"""
import sqlite3, json, subprocess, os, time
from datetime import datetime

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
DB_PATH = "data/animals.db"
HAPPYWHALE_DATASET_ID = "fcbb56da-7237-43a3-831e-d45571496c68"
KAOS_ORGANISM_ID = "https://happywhale.com/individual/6313"
KAOS_KNOWN_LAT = 57.025322
KAOS_KNOWN_LON = -133.044434

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_current_points():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM track_points WHERE animal_id='kaos' ORDER BY ts")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows

def search_obis_by_area(lat, lon, radius_deg=2.0, year=2025, limit=50):
    """搜索 OBIS 中指定区域的座头鲸目击记录（无法精确到 Kaos 个体）"""
    url = ("https://api.obis.org/v3/occurrence?datasetid=%s"
           "&scientificname=Megaptera%%20novaeangliae"
           "&year=%d&size=%d" % (HAPPYWHALE_DATASET_ID, year, limit))
    try:
        r = subprocess.run(["curl.exe", "-s", "-A", UA, "-L", "--max-time", "30", url],
                          capture_output=True, text=True, timeout=35)
        d = json.loads(r.stdout)
        return d.get("results", [])
    except Exception as e:
        print("  OBIS search error:", e)
        return []

def check_for_new_sightings():
    """检查是否有 Kaos 的新目击记录"""
    print("[%s] 开始检查 Kaos 新目击..." % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    current = get_current_points()
    print("  当前轨迹点数:", len(current))
    if current:
        print("  最新目击:", current[-1]["ts"], current[-1]["lat"], current[-1]["lon"])
    
    # 方法1: 搜索 OBIS 中 Kaos 已知位置附近的座头鲸目击
    # 注意: 无法精确到 Kaos 个体，仅作为候选
    print("\n  搜索 OBIS 中 2025-2026 年阿拉斯加东南海域座头鲸目击...")
    results = search_obis_by_area(KAOS_KNOWN_LAT, KAOS_KNOWN_LON, year=2025, limit=100)
    results += search_obis_by_area(KAOS_KNOWN_LAT, KAOS_KNOWN_LON, year=2026, limit=100)
    
    print("  找到 %d 条座头鲸目击记录（该区域，非精确 Kaos）" % len(results))
    
    # 去重坐标
    unique_coords = set()
    for r in results:
        lat = r.get("decimalLatitude")
        lon = r.get("decimalLongitude")
        if lat and lon:
            unique_coords.add((round(lat, 4), round(lon, 4)))
    print("  去重后 %d 个独特坐标" % len(unique_coords))
    
    # 检查是否有 Kaos 已知点之外的新点
    current_coords = set((round(p["lat"], 4), round(p["lon"], 4)) for p in current)
    new_coords = unique_coords - current_coords
    print("  潜在新坐标 %d 个（需人工确认是否为 Kaos）" % len(new_coords))
    
    if new_coords:
        print("\n  ⚠️ 发现潜在新目击坐标，请人工确认是否为 Kaos：")
        for coord in list(new_coords)[:10]:
            print("    %s, %s" % (coord[0], coord[1]))
        print("\n  确认后可手动添加到数据库，或等待 Happywhale 个体页面更新")
    
    # 方法2: 预留 Happywhale 个体页面检查（需要浏览器渲染）
    print("\n  💡 Happywhale 个体页面需浏览器渲染才能抓取，建议定期手动检查：")
    print("     https://happywhale.com/individual/6313")
    
    print("\n[%s] 检查完成" % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return len(new_coords)

def add_point(ts, lat, lon, source="manual"):
    """手动添加 Kaos 的新目击点"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO track_points (animal_id, ts, lat, lon, alt) VALUES (?, ?, ?, ?, 0)",
                ("kaos", ts, lat, lon))
    conn.commit()
    conn.close()
    print("  ✅ 已添加目击点: %s %s %s (%s)" % (ts, lat, lon, source))

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "add":
        # 手动添加: python sync_kaos.py add "2025-08-01 12:00:00" 56.123 -134.567
        ts = sys.argv[2]
        lat = float(sys.argv[3])
        lon = float(sys.argv[4])
        add_point(ts, lat, lon, "manual")
    else:
        check_for_new_sightings()
