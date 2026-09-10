# -*- coding: utf-8 -*-
"""领养页首屏：flex-start 顶部排列 + 断点放宽到 560px"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
P = 'app/static/claim.html'
c = open(P, encoding='utf-8', newline='').read()
c = c.replace('\r\n', '\n')

# 1. 断点 480 -> 560
c = c.replace('@media (max-width: 480px) {', '@media (max-width: 560px) {', 1)
print('断点已改为 560px')

# 2. media 内加 .stage 顶部排列（插在首行注释后）
old_first = '@media (max-width: 560px) {\n  /* 首屏紧凑：不用滚动就能领养 */'
new_first = """@media (max-width: 560px) {
  /* 首屏紧凑：不用滚动就能领养 */
  .stage { justify-content: flex-start; padding-top: 26px; min-height: auto; }"""
assert old_first in c
c = c.replace(old_first, new_first, 1)
print('.stage flex-start 已加')

# 3. 头像进一步缩小
c = c.replace('  .reveal-avatar { width: 112px; height: 112px; }',
              '  .reveal-avatar { width: 100px; height: 100px; }', 1)
c = c.replace('  .reveal-avatar-ring { width: 126px; height: 126px; }',
              '  .reveal-avatar-ring { width: 114px; height: 114px; }', 1)
print('头像已缩小')

open(P, 'w', encoding='utf-8', newline='\n').write(c)
print('完成')
