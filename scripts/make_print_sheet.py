# -*- coding: utf-8 -*-
"""
A4 二维码打印拼版
==================
用法：python scripts/make_print_sheet.py

- 读取 data/qrcodes/*.png
- 拼成 A4（300dpi）打印稿：每页 10 个二维码（5 列 × 2 行），带码号
- 输出到 data/print_sheets/sheet_N.png，打印后沿裁切线裁剪即可贴到吊牌/卡片上
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PIL import Image, ImageDraw, ImageFont  # noqa: E402

import config  # noqa: E402

A4_W, A4_H = 2480, 3508          # 300dpi
MARGIN = 120                     # 页边距
COLS, ROWS = 5, 2                # 每页 5×2 = 10 个
QR_SIZE = 420                    # 二维码打印尺寸（约 3.5cm）
LABEL_H = 130                    # 码号文字区
GAP = 40


def main():
    files = sorted(
        f for f in os.listdir(config.QRCODE_DIR) if f.lower().endswith(".png") and f != "codes.json"
    )
    if not files:
        print("没有找到二维码 PNG，请先运行 scripts/generate_codes.py")
        return

    out_dir = os.path.join(config.DATA_DIR, "print_sheets")
    os.makedirs(out_dir, exist_ok=True)

    # 尝试加载中文字体
    font_paths = [
        r"C:\Windows\Fonts\msyh.ttc",   # 微软雅黑
        r"C:\Windows\Fonts\simhei.ttf",
    ]
    font = None
    for fp in font_paths:
        if os.path.exists(fp):
            font = ImageFont.truetype(fp, 64)
            break
    if font is None:
        font = ImageFont.load_default()

    cell_w = (A4_W - 2 * MARGIN - (COLS - 1) * GAP) // COLS
    cell_h = (A4_H - 2 * MARGIN - (ROWS - 1) * GAP) // ROWS

    pages = [files[i:i + COLS * ROWS] for i in range(0, len(files), COLS * ROWS)]
    for pi, page_files in enumerate(pages):
        sheet = Image.new("RGB", (A4_W, A4_H), "white")
        draw = ImageDraw.Draw(sheet)

        for i, name in enumerate(page_files):
            r, c = divmod(i, COLS)
            x = MARGIN + c * (cell_w + GAP)
            y = MARGIN + r * (cell_h + GAP)

            qr = Image.open(os.path.join(config.QRCODE_DIR, name)).convert("RGB")
            qr = qr.resize((QR_SIZE, QR_SIZE))
            qx = x + (cell_w - QR_SIZE) // 2
            qy = y + (cell_h - QR_SIZE - LABEL_H) // 2
            sheet.paste(qr, (qx, qy))

            code_text = name[:-4]
            label_y = qy + QR_SIZE + 18
            draw.text((x + cell_w // 2, label_y), code_text, fill=(20, 20, 20), font=font, anchor="mm")

            # 裁切辅助线
            lw = 6
            gray = (150, 150, 150)
            for cx, cy, dx, dy in [
                (x, y, 1, 1), (x + cell_w, y, -1, 1),
                (x, y + cell_h, 1, -1), (x + cell_w, y + cell_h, -1, -1),
            ]:
                draw.line([(cx + dx * 0, cy), (cx + dx * 90, cy)], fill=gray, width=lw)
                draw.line([(cx, cy + dy * 0), (cx, cy + dy * 90)], fill=gray, width=lw)

        out = os.path.join(out_dir, f"sheet_{pi + 1}.png")
        sheet.save(out)
        print(f"打印页：{out}（{len(page_files)} 个二维码）")

    print(f"完成：共 {len(files)} 个二维码，{len(pages)} 页，输出目录 {out_dir}")


if __name__ == "__main__":
    main()
