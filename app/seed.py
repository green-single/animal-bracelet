# -*- coding: utf-8 -*-
"""
种子数据：5 只示例动物 + 模拟轨迹
=================================
当前数据为「示例数据」：轨迹由程序模拟生成，用于把系统完整跑通、验证体验。
接入真实数据：注册 Movebank 下载 CSV 后运行 scripts/import_movebank_csv.py 替换。

照片来源：Wikimedia Commons（CC 协议），仅作示例配图，页面会标注来源。
"""
import datetime
import json
import os
import random

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import database  # noqa: E402

ANIMALS = [
    {
        "id": "ava",
        "name": "Ava",
        "species": "绿海龟",
        "species_en": "Green Sea Turtle",
        "story": (
            "她出生在加勒比海某片沙滩的一个夜晚，三十多年后，她仍然记得回家的路。"
            "每年繁殖季，Ava 都会从觅食海域游回出生地附近产卵——海龟的导航能力至今让科学家着迷："
            "磁场、洋流、嗅觉可能都在起作用。示例数据里她的航线是模拟的，但真实的绿海龟跨海迁徙远比这漫长。"
        ),
        "region": {"lat": 21.5, "lon": -77.0, "drift_lat": -1.8, "drift_lon": 3.5, "step": 0.22, "alt": 0},
        "region_label": "加勒比海域 · 古巴附近",
        "photos": [
            {"url": "/static/assets/photos/ava_1.jpg", "license": "CC BY-SA 4.0", "credit": "Wikimedia Commons"},
            {"url": "/static/assets/photos/ava_2.jpg", "license": "CC BY-SA 4.0", "credit": "Wikimedia Commons"},
            {"url": "/static/assets/photos/ava_3.jpg", "license": "CC BY-SA 4.0", "credit": "Wikimedia Commons"},
            {"url": "/static/assets/photos/ava_4.jpg", "license": "CC BY-SA 4.0", "credit": "Wikimedia Commons"},
            {"url": "/static/assets/photos/ava_5.jpg", "license": "CC BY-SA 4.0", "credit": "Wikimedia Commons"},
        ],
    },
    {
        "id": "koa",
        "name": "Koa",
        "species": "大白鲨",
        "species_en": "Great White Shark",
        "story": (
            "Koa 是蒙特雷湾的常客。大白鲨不是电影里的「杀手」——它们是温血动物，为了维持体温必须持续捕食，"
            "所以总沿着海豹和海狮聚集的海岸巡游。科学家用背鳍上的标签追踪它们，发现成年大白鲨会做数千公里的"
            "跨洋旅行，甚至往返于加利福尼亚和夏威夷之间。"
        ),
        "region": {"lat": 36.6, "lon": -122.5, "drift_lat": -2.2, "drift_lon": 0.4, "step": 0.2, "alt": 0},
        "region_label": "太平洋东部 · 美国加州外海",
        "photos": [
            {"url": "/static/assets/photos/koa_1.jpg", "license": "CC BY 2.0", "credit": "Terry Goss / Wikimedia Commons"},
            {"url": "/static/assets/photos/koa_2.jpg", "license": "CC BY 2.5", "credit": "Wikimedia Commons"},
            {"url": "/static/assets/photos/koa_3.jpg", "license": "CC BY 2.0", "credit": "Wikimedia Commons"},
            {"url": "/static/assets/photos/koa_4.jpg", "license": "CC BY 2.0", "credit": "Wikimedia Commons"},
            {"url": "/static/assets/photos/koa_5.jpg", "license": "CC BY 2.0", "credit": "Wikimedia Commons"},
        ],
    },
    {
        "id": "tembo",
        "name": "Tembo",
        "species": "非洲象",
        "species_en": "African Bush Elephant",
        "story": (
            "Tembo 是肯尼亚安博塞利的一头成年公象。大象的记忆力不只是传说：象群会记住水源地和危险区域，"
            "首领母象的智慧决定全家的生死。公象成年后会离开象群独自游荡。每头象每天要喝上百升水、"
            "吃掉上百公斤植物，所以它们的活动范围远比想象中大——安博塞利的雨季和旱季，象群会来回迁徙找水和草。"
        ),
        "region": {"lat": -2.65, "lon": 37.25, "drift_lat": 0.05, "drift_lon": 0.05, "step": 0.028, "alt": 1200},
        "region_label": "非洲 · 肯尼亚安博塞利",
        "photos": [
            {"url": "/static/assets/photos/tembo_1.jpg", "license": "CC BY 2.0", "credit": "Wikimedia Commons"},
            {"url": "/static/assets/photos/tembo_2.jpg", "license": "CC BY-SA 4.0", "credit": "Diego Delso / Wikimedia Commons"},
            {"url": "/static/assets/photos/tembo_3.jpg", "license": "CC BY 2.0", "credit": "Wikimedia Commons"},
            {"url": "/static/assets/photos/tembo_4.jpg", "license": "CC BY 2.0", "credit": "Wikimedia Commons"},
            {"url": "/static/assets/photos/tembo_5.jpg", "license": "CC BY 2.0", "credit": "Wikimedia Commons"},
        ],
    },
    {
        "id": "pippin",
        "name": "Pippin",
        "species": "帝企鹅",
        "species_en": "Emperor Penguin",
        "story": (
            "帝企鹅是唯一在南极冬季繁殖的鸟类。Pippin 的故事从冰上开始：企鹅爸爸把蛋放在脚背上孵整整两个月，"
            "不吃不喝，等妈妈带着食物回来交接班。南极的冬天没有阳光，气温可以低到零下 60 度——"
            "它们挤成一圈，轮流换到外圈挡风，用体温互相取暖。"
        ),
        "region": {"lat": -74.5, "lon": -45.0, "drift_lat": -1.2, "drift_lon": 4.5, "step": 0.28, "alt": 0},
        "region_label": "南极洲 · 威德尔海",
        "photos": [
            {"url": "/static/assets/photos/pippin_1.jpg", "license": "CC BY 2.0", "credit": "Wikimedia Commons"},
            {"url": "/static/assets/photos/pippin_2.jpg", "license": "CC BY-SA 4.0", "credit": "Wikimedia Commons"},
            {"url": "/static/assets/photos/pippin_3.jpg", "license": "CC BY 2.0", "credit": "Wikimedia Commons"},
            {"url": "/static/assets/photos/pippin_4.jpg", "license": "CC BY 2.0", "credit": "Wikimedia Commons"},
            {"url": "/static/assets/photos/pippin_5.jpg", "license": "CC BY 2.0", "credit": "Wikimedia Commons"},
        ],
    },
    {
        "id": "nuna",
        "name": "Nuna",
        "species": "北极燕鸥",
        "species_en": "Arctic Tern",
        "story": (
            "Nuna 是地球上迁徙距离最长的动物。北极燕鸥一生往返于北极和南极之间，一年要飞约 7 万公里——"
            "相当于绕地球近两圈。它们不是在逃离寒冷，而是在追逐永不完结的夏天：北半球入秋，就飞向南极的夏天。"
            "太阳几乎从不在这只鸟的世界里落下。"
        ),
        "region": {"lat": 68.0, "lon": -38.0, "drift_lat": -133.0, "drift_lon": 10.0, "step": 0.9, "alt": 0},
        "region_label": "大西洋上空 · 南北极迁徙途中",
        "photos": [
            {"url": "/static/assets/photos/nuna_1.jpg", "license": "CC BY-SA 4.0", "credit": "Andreas Trepte / Wikimedia Commons"},
            {"url": "/static/assets/photos/nuna_2.jpg", "license": "CC BY-SA 4.0", "credit": "Andreas Weith / Wikimedia Commons"},
            {"url": "/static/assets/photos/nuna_3.jpg", "license": "CC BY-SA 4.0", "credit": "Wikimedia Commons"},
            {"url": "/static/assets/photos/nuna_4.jpg", "license": "CC BY-SA 4.0", "credit": "Wikimedia Commons"},
            {"url": "/static/assets/photos/nuna_5.jpg", "license": "CC BY-SA 4.0", "credit": "Wikimedia Commons"},
        ],
    },
]

DATA_NOTE = (
    "示例数据：轨迹为程序模拟生成，用于系统演示；系统支持从 OBIS / Movebank 等公开"
    "真实遥测源自动同步更新，导入真实数据后此标注会变化。"
)


def gen_track(region, n=300, seed=1):
    """带漂移方向的随机游走，模拟一段时间内的移动轨迹（默认 300 点、每天 1 点）。"""
    rng = random.Random(seed)
    lat, lon = region["lat"], region["lon"]
    d_lat, d_lon = region["drift_lat"], region["drift_lon"]
    # 点数变多后缩小单步随机幅度，避免轨迹过散
    step = region["step"] * (0.5 if n > 100 else 1.0)
    alt = region.get("alt", 0)
    t0 = datetime.datetime(2025, 1, 15, 0, 0, 0)
    pts = []
    for i in range(n):
        lat += d_lat / n + rng.uniform(-step, step)
        lon += d_lon / n + rng.uniform(-step, step)
        lat = max(-85.0, min(85.0, lat))
        lon = max(-180.0, min(180.0, lon))
        pts.append((t0 + datetime.timedelta(days=1 * i), round(lat, 5), round(lon, 5), alt))
    return pts


def seed():
    database.init_db()
    conn = database.get_conn()
    conn.execute("DELETE FROM track_points")
    conn.execute("DELETE FROM animals")
    for a in ANIMALS:
        # 照片本地化：直接引用本地静态资源，避免依赖海外 CDN/图床
        photos = a["photos"]
        for i, p in enumerate(photos):
            p["url"] = f"/static/assets/photos/{a['id']}_{i + 1}.jpg"
        conn.execute(
            "INSERT INTO animals (id, name, species, story, origin, data_note, photo_urls, region_label) VALUES (?,?,?,?,?,?,?,?)",
            (a["id"], a["name"], a["species"], a["story"], "example", DATA_NOTE,
             json.dumps(a["photos"], ensure_ascii=False), a.get("region_label", "")),
        )
        pts = gen_track(a["region"], seed=hash(a["id"]) % 10000)
        conn.executemany(
            "INSERT INTO track_points (animal_id, ts, lat, lon, alt) VALUES (?,?,?,?,?)",
            [(a["id"], p[0].strftime("%Y-%m-%d %H:%M:%S"), p[1], p[2], p[3]) for p in pts],
        )
    conn.commit()
    n_animals = conn.execute("SELECT COUNT(*) FROM animals").fetchone()[0]
    n_pts = conn.execute("SELECT COUNT(*) FROM track_points").fetchone()[0]
    conn.close()
    print(f"seed 完成：{n_animals} 只动物，{n_pts} 个轨迹点")


if __name__ == "__main__":
    seed()
