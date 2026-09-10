# -*- coding: utf-8 -*-
"""生成 HAN-1230 新码（本地DB + seed + 二维码）"""
import sqlite3, json, sys, qrcode
from qrcode.constants import ERROR_CORRECT_M
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')

CODE = 'HAN-1230'

# 1. 本地 DB
conn = sqlite3.connect('data/animals.db')
try:
    conn.execute("INSERT INTO claim_codes (code, animal_id, status) VALUES (?, 'turtle', 'unused')", (CODE,))
    conn.commit()
    print('本地DB已插入', CODE)
except Exception as e:
    print('DB插入:', e)
# 确认 unused
r = conn.execute("SELECT code, animal_id, status FROM claim_codes WHERE code=?", (CODE,)).fetchone()
print('状态:', r)

# 2. seed
p = 'data/animals_seed.json'
d = json.load(open(p, encoding='utf-8'))
d['codes'] = [x for x in d['codes'] if x[0] != CODE]
d['codes'].append([CODE, 'turtle', 'unused', None, None])
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('seed已加，码总数:', len(d['codes']))

# 3. 二维码（干净：纯码）
qr = qrcode.QRCode(version=5, error_correction=ERROR_CORRECT_M, box_size=12, border=3)
qr.add_data(f'https://animal-bracelet.onrender.com/c/{CODE}')
qr.make(fit=True)
qimg = qr.make_image(fill_color='black', back_color='white').convert('RGB')
qw, qh = qimg.size
W, H = qw + 24, qh + 24 + 60
img = Image.new('RGB', (W, H), 'white')
img.paste(qimg, (12, 12))
d2 = ImageDraw.Draw(img)
f = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 36)
t = CODE
tb = d2.textbbox((0, 0), t, font=f)
d2.text(((W - (tb[2]-tb[0]))/2, qh + 24 + 6), t, fill='#333333', font=f)
out = f'qrcodes/{CODE}_Lumi专属码.png'
img.save(out)
print('二维码:', out)
