# -*- coding: utf-8 -*-
"""查 main.py 首页路由和领养接口"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
c = open('app/main.py', encoding='utf-8', newline='').read().replace('\r\n','\n')
lines = c.split('\n')
for i, l in enumerate(lines):
    if '@app.get' in l or '@app.post' in l or 'def ' in l:
        print(i+1, l[:130])
