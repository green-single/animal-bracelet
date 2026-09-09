# -*- coding: utf-8 -*-
"""
批量生成领养码 + 二维码
========================
用法：
  python scripts/generate_codes.py                 # 领养码（默认，N_CODES 个，循环分配动物）
  python scripts/generate_codes.py --animal ava    # 只为指定动物生成领养码
  python scripts/generate_codes.py --share ava --count 3   # 生成 3 个"推广码"（扫码直达动物主页，不占用领养名额）

- 领养码：二维码内容 {BASE_URL}/c/{code}，写入 claim_codes 表（一码一次）
- 推广码：二维码内容 {BASE_URL}/animal/{id}，扫码直接看动物主页，适合推广、摆摊、贴海报

注意：
- 部署上线后，先把 config.py 的 BASE_URL 改成正式域名，再重新生成
- 已存在的码不会被重复生成
"""
import argparse
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import qrcode  # noqa: E402

import config  # noqa: E402
from app import database  # noqa: E402

# 去掉易混淆字符
_ALPHABET = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"


def new_code(rng):
    def block(n):
        return "".join(rng.choice(_ALPHABET) for _ in range(n))
    return f"{block(4)}-{block(4)}"


def main():
    ap = argparse.ArgumentParser(description="生成领养码 / 推广码二维码")
    ap.add_argument("--animal", help="只给指定动物生成（id，如 ava）")
    ap.add_argument("--share", help="推广码模式：指定动物 id，扫码直达其主页")
    ap.add_argument("--count", type=int, default=0, help="生成数量（默认取 config.N_CODES）")
    args = ap.parse_args()

    rng = random.SystemRandom()
    database.init_db()
    conn = database.get_conn()

    if args.animal:
        row = conn.execute("SELECT id FROM animals WHERE id=?", (args.animal,)).fetchone()
        if not row:
            print(f"动物 {args.animal} 不存在，可用：", [r["id"] for r in conn.execute("SELECT id FROM animals").fetchall()])
            conn.close()
            return
        animals = [row["id"]]
    else:
        animals = [r["id"] for r in conn.execute("SELECT id FROM animals").fetchall()]
        if not animals:
            print("数据库中还没有动物，请先运行：python -m app.seed")
            conn.close()
            return

    count = args.count or config.N_CODES
    share_mode = bool(args.share)
    target = args.share or (animals[0] if args.animal else None)

    existing = {r["code"] for r in conn.execute("SELECT code FROM claim_codes").fetchall()}
    os.makedirs(config.QRCODE_DIR, exist_ok=True)

    codes_meta = []
    made = 0
    attempts = 0
    while made < count and attempts < count * 50:
        attempts += 1
        code = new_code(rng)
        if code in existing:
            continue
        existing.add(code)

        if share_mode:
            # 推广码：直达动物主页，不写入领养表；独立目录避免混入打印稿
            animal = target
            url = f"{config.BASE_URL}/animal/{animal}"
            sub = os.path.join(config.QRCODE_DIR, "share")
            os.makedirs(sub, exist_ok=True)
            fname = f"share_{animal}_{code}.png"
            path = os.path.join(sub, fname)
        else:
            animal = animals[made % len(animals)]
            conn.execute(
                "INSERT INTO claim_codes (code, animal_id, status) VALUES (?,?, 'unused')",
                (code, animal),
            )
            url = f"{config.BASE_URL}/c/{code}"
            fname = f"{code}.png"
            path = os.path.join(config.QRCODE_DIR, fname)

        img = qrcode.make(url)
        img = img.convert("RGB").resize((512, 512))
        img.save(path)

        codes_meta.append({
            "code": code, "animal_id": animal, "url": url, "file": path,
            "type": "share" if share_mode else "claim",
        })
        made += 1

    conn.commit()
    conn.close()

    meta_path = os.path.join(config.QRCODE_DIR, "codes.json")
    old = []
    if os.path.exists(meta_path):
        try:
            with open(meta_path, encoding="utf-8") as f:
                old = json.load(f)
        except Exception:
            old = []
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(old + codes_meta, f, ensure_ascii=False, indent=2)

    kind = "推广码" if share_mode else "领养码"
    print(f"已生成 {made} 个{kind}，二维码保存到：{config.QRCODE_DIR}")
    print(f"二维码内容前缀：{config.BASE_URL}/{'animal/' if share_mode else 'c/'}")
    print(f"清单：{meta_path}")
    for m in codes_meta[:5]:
        print(f"  {m['code']} -> {m['animal_id']}  {m['file']}")
    if made > 5:
        print(f"  …… 共 {made} 个")


if __name__ == "__main__":
    main()
