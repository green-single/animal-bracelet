# -*- coding: utf-8 -*-
"""整块替换stuck+load监听"""
P = 'app/static/animal.html'
c = open(P, encoding='utf-8').read()

old_block = """      var stuck = setTimeout(function () {
        if (srcIdx < tileSources.length - 1) { srcIdx++; addTiles(); }
      }, 6000);
      activeLayers.once('load', function () { clearTimeout(stuck); });"""
new_block = """      var stuck = setTimeout(function () {
        if (srcIdx < tileSources.length - 1) { srcIdx++; addTiles(); }
      }, 15000);
      list.forEach(function (cfg, li) { var ll = activeLayers[li]; if (ll) ll.once('load', function () { clearTimeout(stuck); }); });"""

assert old_block in c, 'stuck块未找到'
c = c.replace(old_block, new_block)
open(P, 'w', encoding='utf-8').write(c)
print('OK 换源超时15s + 单图层load监听')
print('15000:', c.count('15000'))
print('单图层监听:', c.count('ll.once'))
