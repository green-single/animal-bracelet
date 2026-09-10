# -*- coding: utf-8 -*-
"""统一LF后替换stuck+load监听，写回LF"""
P = 'app/static/animal.html'
c = open(P, encoding='utf-8', newline='').read()
# 统一成LF处理
has_crlf = '\r\n' in c
c = c.replace('\r\n', '\n')

old_block = """      var stuck = setTimeout(function () {
        if (srcIdx < tileSources.length - 1) { srcIdx++; addTiles(); }
      }, 6000);
      activeLayers.once('load', function () { clearTimeout(stuck); });"""
new_block = """      var stuck = setTimeout(function () {
        if (srcIdx < tileSources.length - 1) { srcIdx++; addTiles(); }
      }, 15000);
      list.forEach(function (cfg, li) { var ll = activeLayers[li]; if (ll) ll.once('load', function () { clearTimeout(stuck); }); });"""

assert old_block in c, 'stuck块未找到(CRLF已转LF)'
c = c.replace(old_block, new_block)
# 写回LF（不转CRLF）
open(P, 'w', encoding='utf-8', newline='\n').write(c)
print('原文件CRLF:', has_crlf, '| 已转LF写回')
print('15000:', c.count('15000'), '| ll.once:', c.count('ll.once'))
