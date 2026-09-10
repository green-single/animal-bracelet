# -*- coding: utf-8 -*-
"""二维码加标注：动物名+码"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image, ImageDraw, ImageFont

animals = [
    ('Lumi 欧斑鸠', 'KHYM-NVWZ'),
    ('Noé 白鹳', 'ESZK-4MQA'),
    ('Silver 银鸥', '5EBQ-TRN6'),
    ('Athos 红鸢', 'VDDN-8VQM'),
    ('Mel 蜂鹰', 'FC2U-RTD8'),
    ('Koa 大白鲨(示例)', 'MMMD-579M'),
]

# 找中文字体
font_candidates = [
    'C:/Windows/Fonts/msyh.ttc',      # 微软雅黑
    'C:/Windows/Fonts/simhei.ttf',    # 黑体
    'C:/Windows/Fonts/simsun.ttc',    # 宋体
]
fp = None
for f in font_candidates:
    if os.path.exists(f):
        fp = f
        break
print('字体:', fp)

os.makedirs('qrcodes', exist_ok=True)
for name, code in animals:
    src = 'qrcodes/_raw_%s.png' % code
    # 先生成纯二维码
    import qrcode
    from qrcode.constants import ERROR_CORRECT_M
    url = 'https://animal-bracelet.onrender.com/c/' + code
    qr = qrcode.QRCode(version=5, error_correction=ERROR_CORRECT_M, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    qr.make_image(fill_color='black', back_color='white').save(src)

    img = Image.open(src).convert('RGB')
    W, H = img.size
    # 底部加文字条
    bar = 110
    canvas = Image.new('RGB', (W, H + bar), 'white')
    canvas.paste(img, (0, 0))
    d = ImageDraw.Draw(canvas)
    f_title = ImageFont.truetype(fp, 44) if fp else ImageFont.load_default()
    f_code = ImageFont.truetype(fp, 34) if fp else ImageFont.load_default()
    # 名字居中
    tb = d.textbbox((0, 0), name, font=f_title)
    d.text(((W - (tb[2]-tb[0])) / 2, H + 6), name, fill='black', font=f_title)
    # 码居中
    tb2 = d.textbbox((0, 0), '领养码 ' + code, font=f_code)
    d.text(((W - (tb2[2]-tb2[0])) / 2, H + 62), '领养码 ' + code, fill='#555555', font=f_code)

    fn = 'qrcodes/%s_%s.png' % (name.replace(' ', '').replace('(示例)', ''), code)
    canvas.save(fn)
    print(fn)
print('完成')
