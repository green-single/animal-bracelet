# -*- coding: utf-8 -*-
"""修复年份筛选后轨迹消失：idx重置为末尾而非0"""
P = 'app/static/animal.html'
NL = chr(10)
c = open(P, encoding='utf-8').read()
lines = c.split(NL)

old = [
    "          timestamps = filteredTs;",
    "          idx = 0;",
    "          var slider = document.getElementById('tlSlider');",
    "          slider.max = points.length - 1;",
    "          slider.value = 0;",
]
new = [
    "          timestamps = filteredTs;",
    "          idx = points.length - 1;",
    "          var slider = document.getElementById('tlSlider');",
    "          slider.max = points.length - 1;",
    "          slider.value = points.length - 1;",
]
found = False
for i in range(len(lines) - len(old)):
    if all(lines[i + k].strip() == old[k].strip() for k in range(len(old))):
        lines[i:i + len(old)] = new
        found = True
        break
assert found, '年份筛选段未找到'

c = NL.join(lines)
open(P, 'w', encoding='utf-8').write(c)
print('OK 年份筛选修复：筛选后显示完整轨迹')
