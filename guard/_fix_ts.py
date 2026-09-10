# -*- coding: utf-8 -*-
"""修复 timestamps → ts（_runAbcd 作用域变量）"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
P = 'app/static/animal.html'
c = open(P, encoding='utf-8', newline='').read()
c = c.replace('\r\n', '\n')

OLD = "          var lts = timestamps[timestamps.length - 1];"
NEW = "          var lts = ts[ts.length - 1];"
if OLD in c:
    c = c.replace(OLD, NEW, 1)
    print('已修复')
else:
    print('锚点未找到')
open(P, 'w', encoding='utf-8', newline='\n').write(c)
