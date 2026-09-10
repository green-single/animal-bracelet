# -*- coding: utf-8 -*-
"""换源超时 6s→15s（Esri慢不误切）+ 首位Esri瓦片成功即取消超时"""
P = 'app/static/animal.html'
NL = chr(10)
c = open(P, encoding='utf-8').read()
lines = c.split(NL)

old = "      var stuck = setTimeout(function () {"
new = "      var stuck = setTimeout(function () {"
found = False
for i, l in enumerate(lines):
    if 'var stuck = setTimeout' in l:
        # 改超时值 6000 → 15000
        lines[i] = lines[i].replace('6000', '15000')
        found = True
        break
assert found, 'stuck未找到'

# 把 once('load') 改为每个图层都监听 load（任一成功即取消超时）
old_load = "      activeLayers.once('load', function () { clearTimeout(stuck); });"
new_load = "      list.forEach(function (cfg, li) { var ll = activeLayers[li]; if (ll) ll.once('load', function () { clearTimeout(stuck); }); });"
found = False
for i, l in enumerate(lines):
    if old_load in l:
        lines[i] = l.replace(old_load, new_load)
        found = True
        break
assert found, 'load监听未找到'

c = NL.join(lines)
open(P, 'w', encoding='utf-8').write(c)
print('OK 换源超时15s+单图层load监听')
print('15000:', c.count('15000'))
print('每图层load:', c.count('ll.once'))
