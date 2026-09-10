# -*- coding: utf-8 -*-
"""claim.html 加 viewport meta（手机端修复根因）"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
P = 'app/static/claim.html'
c = open(P, encoding='utf-8', newline='').read()
c = c.replace('\r\n', '\n')
if '<meta name="viewport"' in c:
    print('已有 viewport，跳过')
else:
    anchor = '<meta charset="UTF-8">'
    assert anchor in c
    vp = '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">'
    c = c.replace(anchor, anchor + '\n  ' + vp, 1)
    open(P, 'w', encoding='utf-8', newline='\n').write(c)
    print('viewport 已加')
