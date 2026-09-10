# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
c = open('app/static/animal.html', encoding='utf-8', newline='').read()
i = c.find('function showTab')
if i < 0:
    i = c.find('showTab = function')
print('showTab定义:', repr(c[i:i+700]) if i >= 0 else '未找到')
