# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
c = open('app/static/animal.html', encoding='utf-8').read()
for m in re.finditer(r'\.photo-item[^{]*\{[^}]*\}', c):
    print(repr(m.group()[:300]))
    print('---')
