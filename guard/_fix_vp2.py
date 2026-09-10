# -*- coding: utf-8 -*-
"""修复残缺 viewport meta（animal/claim 页，被apple-touch-icon插入破坏）"""
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

for page in ['app/static/animal.html', 'app/static/claim.html']:
    c = open(page, encoding='utf-8', newline='').read()
    c = c.replace('\r\n', '\n')
    # 修复残缺模式1: <meta name="viewport" <link rel="apple-touch-icon" ...>
    pat1 = re.compile(r'<meta name="viewport"\s*<link[^>]*rel="apple-touch-icon"[^>]*>')
    if pat1.search(c):
        c = pat1.sub('<meta name="viewport" content="width=device-width, initial-scale=1.0">\n  <link rel="apple-touch-icon" href="/icons/apple-touch-icon.png">', c)
        print(page, '修复残缺viewport(appl-icon)')
    # 修复残缺模式2: <meta name="viewport" 后面直接换行跟其他（无闭合）
    pat2 = re.compile(r'<meta name="viewport"\s*\n\s*(?!content=)')
    if pat2.search(c):
        c = pat2.sub('<meta name="viewport" content="width=device-width, initial-scale=1.0">\n  ', c)
        print(page, '修复残缺viewport(通用)')
    # 确认最终有正确 viewport
    ok = re.search(r'<meta name="viewport" content="[^"]+"', c)
    if not ok:
        # 完全没有 viewport → 加
        anchor = '<meta charset="UTF-8">'
        if anchor in c:
            c = c.replace(anchor, anchor + '\n  <meta name="viewport" content="width=device-width, initial-scale=1.0">', 1)
            print(page, '补全 viewport')
    open(page, 'w', encoding='utf-8', newline='\n').write(c)
print('完成')
