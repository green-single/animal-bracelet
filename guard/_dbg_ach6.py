# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
c = open('app/static/animal.html', encoding='utf-8').read()
i = c.find('(achId, achName) {')
print(c[i-200:i+80])
# 找所有调用点
import re
for m in re.finditer(r'unlockAchievement', c):
    print('@', m.start(), ':', c[m.start()-40:m.start()+60].replace('\n', ' ')[:100])
    print()
