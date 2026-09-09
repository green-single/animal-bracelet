# -*- coding: utf-8 -*-
import re
c = open('app/static/animal.html', encoding='utf-8').read()

i = c.find('class="quiz-section"')
print('quiz-section HTML@', i)
print()
# 找主要结构
pats = ['class="tab-bar"', 'id="tab-', 'class="tab-content', 'tablbl', 'data-tab=', 'tab-lbl']
seen = set()
for kw in pats:
    for m in re.finditer(re.escape(kw), c):
        pos = m.start()
        ctx = c[max(0, pos - 50):pos + 90].replace('\n', ' ')[:150]
        print(kw, '@', pos)
        print('   ', ctx)
        break
print()
# 列出所有 tab 相关 id
ids = re.findall(r'id="(tab[^"]*)"', c)
print('tab ids:', ids[:30])
# 知识问答在哪个容器里？往前找最近的容器开头
seg = c[:i]
opens = [m.start() for m in re.finditer(r'<div[^>]*id="[^"]*"[^>]*>', seg)]
if opens:
    last = opens[-1]
    print('\n知识问答所在容器:', c[last:last + 120].replace('\n', ' '))
# tab-bar 结构
j = c.find('class="tab-bar"')
if j > 0:
    print('\ntab-bar HTML:', c[j:j + 700].replace('\n', ' ')[:700])
