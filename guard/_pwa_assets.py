# -*- coding: utf-8 -*-
"""生成 PWA 图标（爪印）+ manifest.json"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image, ImageDraw

os.makedirs('app/static/icons', exist_ok=True)

def make_icon(size, out):
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    r = int(size * 0.2)
    # 深绿圆角方底
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=r, fill=(11, 46, 29, 255))
    # 内圈浅绿描边
    m = int(size * 0.07)
    d.ellipse([m, m, size - m, size - m], outline=(64, 150, 108, 255), width=int(size * 0.028))
    # 白色爪印
    c = (216, 243, 220, 255)
    w = size / 512.0
    # 掌垫（下方大椭圆）
    d.ellipse([176 * w, 302 * w, 336 * w, 436 * w], fill=c)
    # 4 趾
    d.ellipse([148 * w, 192 * w, 224 * w, 292 * w], fill=c)
    d.ellipse([238 * w, 168 * w, 314 * w, 268 * w], fill=c)
    d.ellipse([322 * w, 214 * w, 388 * w, 296 * w], fill=c)
    d.ellipse([236 * w, 252 * w, 288 * w, 320 * w], fill=c)
    img.save(out)
    print(out, size)

make_icon(512, 'app/static/icons/icon-512.png')
make_icon(192, 'app/static/icons/icon-192.png')
make_icon(180, 'app/static/icons/apple-touch-icon.png')

# manifest.json
manifest = {
    "name": "动物追踪手环 · 我的动物",
    "short_name": "动物手环",
    "description": "扫描手环二维码，领养一只真实迁徙的动物，跟随它的足迹。",
    "start_url": "/",
    "scope": "/",
    "display": "standalone",
    "background_color": "#0b2e1d",
    "theme_color": "#12796F",
    "icons": [
        {"src": "/icons/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
        {"src": "/icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"}
    ]
}
import json
open('app/static/manifest.json', 'w', encoding='utf-8', newline='\n').write(json.dumps(manifest, ensure_ascii=False, indent=2))
print('manifest.json 已写入')
