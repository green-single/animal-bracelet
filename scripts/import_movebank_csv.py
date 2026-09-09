# -*- coding: utf-8 -*-
"""
从 Movebank CSV 导入真实动物轨迹
=================================
用法：
  python scripts/import_movebank_csv.py --csv 数据.csv --id myturtle --name "Maya" --species "绿海龟" [--story "..."] [--limit 200] [--step 1]

参数：
  --csv      Movebank 导出的 event CSV（必填）
  --id       动物 ID（必填，字母数字，作为链接里的唯一标识）
  --name     动物名字（必填）
  --species  物种中文名（必填）
  --story    动物故事/档案（可选，不填则用默认说明）
  --limit    最多导入多少个轨迹点（默认全部）
  --step     抽样间隔，1=全部，2=隔一个取一个（默认 1）

Movebank 下载步骤（详见 README）：
  1. 注册 Movebank 账号，在 Tracking Data Map 找到公开可下载的研究
  2. 接受数据集许可条款后，下载该研究的 Event（.csv）
  3. 运行本脚本导入（会自动识别 timestamp / location-long / location-lat 等列名）
"""
import argparse
import csv
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import database  # noqa: E402

TS_KEYS = ["timestamp", "event-time", "datetime", "date_time", "time"]
LON_KEYS = ["location-long", "longitude", "lon", "long"]
LAT_KEYS = ["location-lat", "latitude", "lat"]
ALT_KEYS = ["height-above-msl", "altitude", "alt", "height"]


def find_key(header, keys):
    lowered = {h.strip().lower(): h for h in header}
    for k in keys:
        if k in lowered:
            return lowered[k]
    return None


def main():
    ap = argparse.ArgumentParser(description="导入 Movebank 轨迹 CSV")
    ap.add_argument("--csv", required=True, help="Movebank event CSV 路径")
    ap.add_argument("--id", required=True, help="动物 ID（字母数字）")
    ap.add_argument("--name", required=True, help="动物名字")
    ap.add_argument("--species", required=True, help="物种中文名")
    ap.add_argument("--story", default="", help="动物故事（可选）")
    ap.add_argument("--limit", type=int, default=0, help="最多导入点数（0=全部）")
    ap.add_argument("--step", type=int, default=1, help="抽样间隔")
    args = ap.parse_args()

    if not os.path.exists(args.csv):
        print(f"文件不存在：{args.csv}")
        return

    with open(args.csv, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames or []
        ts_k = find_key(header, TS_KEYS)
        lon_k = find_key(header, LON_KEYS)
        lat_k = find_key(header, LAT_KEYS)
        alt_k = find_key(header, ALT_KEYS)
        if not (ts_k and lon_k and lat_k):
            print("无法识别列名。需要时间戳、经度、纬度三列。")
            print(f"识别到的列：{header}")
            return

        rows = []
        for row in reader:
            try:
                ts = row[ts_k].strip()
                lon = float(row[lon_k])
                lat = float(row[lat_k])
            except (ValueError, KeyError, TypeError):
                continue
            alt = 0.0
            if alt_k and row.get(alt_k):
                try:
                    alt = float(row[alt_k])
                except ValueError:
                    alt = 0.0
            rows.append((ts, lat, lon, alt))

    # 去重 + 按时间排序
    seen = set()
    uniq = []
    for r in rows:
        if r[0] in seen:
            continue
        seen.add(r[0])
        uniq.append(r)
    uniq.sort(key=lambda r: r[0])

    # 抽样
    if args.step > 1:
        uniq = uniq[:: args.step]
    if args.limit > 0:
        uniq = uniq[: args.limit]

    if len(uniq) < 2:
        print("有效轨迹点不足 2 个，无法导入。")
        return

    story = args.story or (
        f"这是一只由 Movebank 公开研究数据导入的 {args.species}。"
        "它的轨迹由科研团队佩戴追踪器记录，位置数据可能存在延迟。"
    )

    database.init_db()
    conn = database.get_conn()
    conn.execute(
        "INSERT OR REPLACE INTO animals (id, name, species, story, origin, data_note, photo_urls, region_label) "
        "VALUES (?,?,?,?, 'movebank', ?, '[]', '')",
        (
            args.id,
            args.name,
            args.species,
            story,
            f"数据来源：Movebank 公开研究（{os.path.basename(args.csv)}），共 {len(uniq)} 个定位点。",
        ),
    )
    conn.execute("DELETE FROM track_points WHERE animal_id = ?", (args.id,))
    conn.executemany(
        "INSERT INTO track_points (animal_id, ts, lat, lon, alt) VALUES (?,?,?,?,?)",
        [(args.id, r[0], r[1], r[2], r[3]) for r in uniq],
    )
    conn.commit()
    conn.close()

    print(f"导入完成：{args.name}（{args.species}），{len(uniq)} 个轨迹点")
    print(f"时间范围：{uniq[0][0]}  →  {uniq[-1][0]}")
    print("注意：导入后记得为该动物补充照片（可在数据库中更新 photo_urls），"
          "并在生成领养码前运行 python scripts/generate_codes.py 分配新码。")


if __name__ == "__main__":
    main()
