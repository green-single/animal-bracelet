# -*- coding: utf-8 -*-
"""Lumi han1229 专属二维码卡片"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image, ImageDraw, ImageFont
import qrcode
from qrcode.constants import ERROR_CORRECT_M

fp = 'C:/Windows/Fonts/msyh.ttc'
f_big = ImageFont.truetype(fp, 56)
f_mid = ImageFont.truetype(fp, 34)
f_small = ImageFont.truetype(fp, 26)

GREEN = (11, 46, 29, 255)
CREAM = (244, 243, 238, 255)
GOLD = (224, 212, 143, 255)

codes = [('KHYM-NVWZ', '专属 · Lumi 欧斑鸠'), ('2SKS-SPTN', '专属 · Lumi 欧斑鸠'), ('4SYS-R6F8', '专属 · Lumi 欧斑鸠')]

os.makedirs('qrcodes', exist_ok=True)
for code, sub in codes:
    # 二维码
    qr = qrcode.QRCode(version=5, error_correction=ERROR_CORRECT_M, box_size=9, border=3)
    qr.add_data('https://animal-bracelet.onrender.com/c/' + code)
    qr.make(fit=True)
    qimg = qr.make_image(fill_color='black', back_color='white').convert('RGB')
    qw, qh = qimg.size

    # 卡片：700 宽
    W = 700
    pad = 40
    H = pad * 2 + qh + 40 + 150  # 上方留名区+han + 二维码 + 下方码区
    img = Image.new('RGB', (W, H), GREEN)
    d = ImageDraw.Draw(img)

    # 顶部：动物名
    t = 'Lumi · 欧斑鸠'
    tb = d.textbbox((0, 0), t, font=f_mid)
    d.text(((W - (tb[2] - tb[0])) / 2, pad), t, fill=CREAM, font=f_mid)

    # han1229 大字
    t2 = 'han1229'
    tb2 = d.textbbox((0, 0), t2, font=f_big)
    d.text(((W - (tb2[2] - tb2[0])) / 2, pad + 48), t2, fill=GOLD, font=f_big)

    # 二维码（白底区）
    qx = (W - qw) // 2
    qy = pad + 48 + 78
    d.rectangle([qx - 14, qy - 14, qx + qw + 14, qy + qh + 14], fill='white')
    img.paste(qimg, (qx, qy))

    # 码
    t3 = '领养码 ' + code
    tb3 = d.textbbox((0, 0), t3, font=f_mid)
    d.text(((W - (tb3[2] - tb3[0])) / 2, qy + qh + 30), t3, fill=CREAM, font=f_mid)

    fn = 'qrcodes/Lumi_han1229_%s.png' % code[:4]
    img.save(fn)
    print(fn, img.size)
print('完成')
