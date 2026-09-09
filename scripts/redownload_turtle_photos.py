# -*- coding: utf-8 -*-
"""
重新下载欧斑鸠的有效照片，并检查所有动物的照片
"""
import subprocess
import os
from PIL import Image

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
PHOTO_DIR = "app/static/assets/photos"

# 欧斑鸠的有效图片URL（从Wikimedia Commons搜索，确保是真实的JPEG）
turtle_photo_urls = [
    "https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/European_Turtle_Dove_%28Streptopelia_turtur%29_%2832623374562%29.jpg/800px-European_Turtle_Dove_%28Streptopelia_turtur%29_%2832623374562%29.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Streptopelia_turtur_-British_Wildlife_Centre%2C_Surrey%2C_England-8a_%281%29.jpg/800px-Streptopelia_turtur_-British_Wildlife_Centre%2C_Surrey%2C_England-8a_%281%29.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Turtle_Dove_%28Streptopelia_turtur%29_%2816933402781%29.jpg/800px-Turtle_Dove_%28Streptopelia_turtur%29_%2816933402781%29.jpg",
]

print("=" * 60)
print("重新下载欧斑鸠照片")
print("=" * 60)

for i, url in enumerate(turtle_photo_urls[:3]):
    filename = f"turtle_{i+1}.jpg"
    filepath = os.path.join(PHOTO_DIR, filename)
    print(f"\n下载 {filename}...")
    print(f"  URL: {url[:80]}...")
    
    r = subprocess.run(
        ["curl.exe", "-s", "-A", UA, "-L", "--max-time", "60", "-o", filepath, url],
        capture_output=True, timeout=65
    )
    
    if os.path.exists(filepath) and os.path.getsize(filepath) > 10000:
        # 验证图片是否有效
        try:
            img = Image.open(filepath)
            print(f"  ✅ 下载成功并验证有效: {img.size} {img.mode} ({os.path.getsize(filepath)} bytes)")
        except Exception as e:
            print(f"  ❌ 图片无效: {e}")
            # 删除损坏的文件
            os.remove(filepath)
    else:
        print(f"  ❌ 下载失败或文件太小")
        if os.path.exists(filepath):
            print(f"  文件大小: {os.path.getsize(filepath)} bytes")

print("\n" + "=" * 60)
print("验证所有动物的照片")
print("=" * 60)

all_photos = [
    ("noe", ["noe_1.jpg", "noe_2.jpg", "noe_3.jpg", "noe_4.jpg", "noe_5.jpg"]),
    ("turtle", ["turtle_1.jpg", "turtle_2.jpg", "turtle_3.jpg"]),
    ("koa", ["koa_1.jpg", "koa_2.jpg", "koa_3.jpg", "koa_4.jpg", "koa_5.jpg"]),
]

for animal, photos in all_photos:
    print(f"\n[{animal}]")
    valid_count = 0
    for photo in photos:
        filepath = os.path.join(PHOTO_DIR, photo)
        if os.path.exists(filepath):
            try:
                img = Image.open(filepath)
                print(f"  ✅ {photo}: {img.size} ({os.path.getsize(filepath)} bytes)")
                valid_count += 1
            except Exception as e:
                print(f"  ❌ {photo}: 无效 - {e}")
        else:
            print(f"  ⚠️ {photo}: 文件不存在")
    print(f"  有效照片: {valid_count}/{len(photos)}")

print("\n" + "=" * 60)
print("完成！")
