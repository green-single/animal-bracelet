# -*- coding: utf-8 -*-
"""修复残缺 viewport meta（手机端980px问题根因）"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
P = 'app/static/claim.html'
c = open(P, encoding='utf-8', newline='').read()
c = c.replace('\r\n', '\n')

# 修复残缺 meta（第6-7行）
broken = '<meta name="viewport"\n  <link rel="manifest" href="/manifest.json">'
fixed = '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n  <link rel="manifest" href="/manifest.json">'
if broken in c:
    c = c.replace(broken, fixed, 1)
    print('残缺 viewport 已修复')
else:
    print('未找到残缺模式，检查实际内容')
    import re
    m = re.search(r'<meta name="viewport"[^>]*>', c)
    print('现有 viewport meta:', m.group(0) if m else '无')

open(P, 'w', encoding='utf-8', newline='\n').write(c)
print('完成')
