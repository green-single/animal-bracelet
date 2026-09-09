# -*- coding: utf-8 -*-
"""animal.html 改造：Tab上移 + 知识问答独立成第6个Tab"""
import re

P = 'app/static/animal.html'
c = open(P, encoding='utf-8').read()
orig = c

# 1. CSS: tab-bar 从底部 fixed → 顶部 sticky
old_css = '''  .tab-bar {
    position: fixed; left: 0; right: 0; bottom: 0; z-index: 9000;
    display: flex; background: rgba(255,255,255,.97); backdrop-filter: blur(14px);
    border-top: 1px solid rgba(0,0,0,.08); box-shadow: 0 -6px 24px rgba(0,0,0,.08);
  }'''
new_css = '''  .tab-bar {
    position: sticky; top: 0; z-index: 9000;
    display: flex; background: rgba(255,255,255,.97); backdrop-filter: blur(14px);
    border-bottom: 1px solid rgba(0,0,0,.08); box-shadow: 0 6px 24px rgba(0,0,0,.08);
  }'''
assert old_css in c, 'CSS未找到'
c = c.replace(old_css, new_css)

# 2. tab-main 加 tabQuiz 空容器
old_view = '''<div class="tab-view tab-mine" id="tabMine"></div>
  </div>'''
new_view = '''<div class="tab-view tab-mine" id="tabMine"></div>
    <div class="tab-view tab-quiz" id="tabQuiz"></div>
  </div>'''
assert old_view in c, 'tabMine容器未找到'
c = c.replace(old_view, new_view)

# 3. tab-bar 加"知识"项（成就前）
old_item = '''<div class="tab-item" data-tab="ach"><span class="tab-ico">🏆</span><span class="tab-lbl">成就</span></div>'''
new_item = '''<div class="tab-item" data-tab="quiz"><span class="tab-ico">📚</span><span class="tab-lbl">知识</span></div>
    <div class="tab-item" data-tab="ach"><span class="tab-ico">🏆</span><span class="tab-lbl">成就</span></div>'''
assert old_item in c, '成就tab项未找到'
c = c.replace(old_item, new_item)

# 4. quiz 渲染目标 → tabQuiz
old_q = 'facts.parentNode.appendChild(quizDiv);'
new_q = "document.getElementById('tabQuiz').appendChild(quizDiv);"
assert old_q in c, 'quiz渲染目标未找到'
c = c.replace(old_q, new_q)

# 5. tab-bar 整块从 body 末尾移到 main 开头
m = re.search(r'<!-- Tab 底部导航 -->\s*<div class="tab-bar" id="tabBar">.*?</div>\s*(?=</body>)', c, re.S)
assert m, 'tab-bar块未找到'
bar_block = m.group(0)
c = c.replace(bar_block, '')
anchor = '<main>\n  <div class="tab-main">'
assert anchor in c, 'main锚点未找到'
c = c.replace(anchor, '<main>\n' + bar_block.strip() + '\n  <div class="tab-main">')

open(P, 'w', encoding='utf-8').write(c)
print('✅ 改造完成')
print('原长度:', len(orig), '→ 新长度:', len(c))
# 校验
print('tabQuiz容器:', 'id="tabQuiz"' in c)
print('知识Tab项:', 'data-tab="quiz"' in c)
print('tab-bar位置main:', c.find('tab-bar') < c.find('tab-main'))
print('quiz目标:', "getElementById('tabQuiz')" in c)
