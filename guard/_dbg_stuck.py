# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
c = open('app/static/animal.html', encoding='utf-8', newline='').read()
c = c.replace('\r\n', '\n')

old_block = """      var stuck = setTimeout(function () {
        if (srcIdx < tileSources.length - 1) { srcIdx++; addTiles(); }
      }, 6000);
      activeLayers.once('load', function () { clearTimeout(stuck); });"""

print('old_block repr:')
print(repr(old_block))
print()
print('文件中是否含 6000):', '6000);' in c)
print('文件中是否含 once load:', "activeLayers.once('load'" in c)
# 从6000开始找
i = c.find('}, 6000);')
print('6000上下文:', repr(c[i-30:i+60]) if i >= 0 else '无')
