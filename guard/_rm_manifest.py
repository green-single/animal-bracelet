# -*- coding: utf-8 -*-
"""彻底方案：animal/claim 页移除 manifest 链接
→ iOS/安卓添加主屏幕必用当前URL（动物页），打开即动物页
"""
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

for page in ['app/static/animal.html', 'app/static/claim.html']:
    c = open(page, encoding='utf-8', newline='').read()
    c = c.replace('\r\n', '\n')
    # 移除 manifest link（可能有多个残留，全部移除）
    c2 = re.sub(r'\s*<link rel="manifest"[^>]*>', '', c)
    # 也移除孤立的残缺 manifest 行（<meta name="viewport" 后跟 <link manifest 的坏结构）
    c2 = re.sub(r'\s*<link rel="manifest"[^>]*/?>', '', c2)
    if c2 != c:
        open(page, 'w', encoding='utf-8', newline='\n').write(c2)
        print(page, 'manifest链接已移除')
    else:
        print(page, '未找到manifest链接，检查')
        for i, l in enumerate(c.split('\n')):
            if 'manifest' in l:
                print(' ', i+1, l[:100])
print('完成')
