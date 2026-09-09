# -*- coding: utf-8 -*-
"""成就弹窗：批量解锁也触发（本次会话仅首次）"""
P = 'app/static/animal.html'
NL = chr(10)
c = open(P, encoding='utf-8').read()
lines = c.split(NL)

# 批量解锁段
old_batch = [
    "          items.forEach(function(item) {",
    "            var ach = item.dataset.ach;",
    "            if (achievements[ach]) {",
    "              item.classList.remove('locked');",
    "              item.classList.add('unlocked');",
    "              unlockedCount++;",
    "            }",
    "          });",
]
new_batch = [
    "          items.forEach(function(item) {",
    "            var ach = item.dataset.ach;",
    "            if (achievements[ach]) {",
    "              item.classList.remove('locked');",
    "              item.classList.add('unlocked');",
    "              unlockedCount++;",
    "              // 弹窗（本次会话仅首次，避免每次刷新都弹）",
    "              try {",
    "                var pKey = 'achPopped_' + animalId;",
    "                if (!sessionStorage.getItem(pKey)) {",
    "                  var ico = item.querySelector('.achievement-icon');",
    "                  var nm = item.querySelector('.achievement-name');",
    "                  window._achQueue.push({ ico: ico ? ico.textContent : '🏅', name: nm ? nm.textContent : ach });",
    "                  if (window._achQueue.length > 3) window._achQueue.splice(0, window._achQueue.length - 3);",
    "                  window._achShowNext();",
    "                }",
    "              } catch(e3) {}",
    "            }",
    "          });",
    "          if (unlockedCount > 0) { try { sessionStorage.setItem('achPopped_' + animalId, '1'); } catch(e4) {} }",
]
found = False
for i in range(len(lines) - len(old_batch)):
    if all(lines[i + k].strip() == old_batch[k].strip() for k in range(len(old_batch))):
        lines[i:i + len(old_batch)] = new_batch
        found = True
        break
assert found, '批量解锁段未找到'

c = NL.join(lines)
open(P, 'w', encoding='utf-8').write(c)
print('OK 批量解锁弹窗完成')
print('批量弹窗触发:', c.count("pKey = 'achPopped_'"))
