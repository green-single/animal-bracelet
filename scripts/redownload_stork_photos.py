# -*- coding: utf-8 -*-
import subprocess, os, urllib.parse

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

def download_wikimedia(filename, outpath, timeout=60):
    """用 Special:FilePath 下载 Wikimedia 图片"""
    url = "https://commons.wikimedia.org/wiki/Special:FilePath/%s" % urllib.parse.quote(filename)
    r = subprocess.run(["curl.exe", "-s", "-A", UA, "-L", "--max-time", str(timeout),
                        "-e", "https://commons.wikimedia.org/", url, "-o", outpath],
                      capture_output=True, timeout=timeout+5)
    return os.path.exists(outpath) and os.path.getsize(outpath) > 10000

# 重新下载失败的 3 张
files_to_download = [
    ("White Stork (Ciconia ciconia) (5).jpg", "app/static/assets/photos/noe_3.jpg"),
    ("Páření čápů bílých.jpg", "app/static/assets/photos/noe_4.jpg"),
    ("White Stork.jpg", "app/static/assets/photos/noe_5.jpg"),
]

for filename, outpath in files_to_download:
    success = download_wikimedia(filename, outpath)
    if success:
        size = os.path.getsize(outpath)
        print("  ✅ %s: %d bytes" % (outpath, size))
    else:
        print("  ❌ %s: FAILED" % outpath)
        # 如果失败，删除空文件
        if os.path.exists(outpath):
            os.remove(outpath)

# 验证所有 5 张
print("\n=== Verifying all photos ===")
for i in range(1, 6):
    path = "app/static/assets/photos/noe_%d.jpg" % i
    if os.path.exists(path):
        size = os.path.getsize(path)
        print("  noe_%d.jpg: %d bytes %s" % (i, size, "✅" if size > 10000 else "⚠️ too small"))
    else:
        print("  noe_%d.jpg: MISSING ❌" % i)
