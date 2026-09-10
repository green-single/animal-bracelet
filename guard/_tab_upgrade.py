# -*- coding: utf-8 -*-
"""Tab 栏优化（v2 简化，避免多行字符串引号陷阱）"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

P = 'app/static/animal.html'
c = open(P, encoding='utf-8', newline='').read()
c = c.replace('\r\n', '\n')
orig = c

# ===== 1. CSS 替换 tab-bar 块 =====
old_css = ".tab-bar {\nposition: sticky; top: 0; z-index: 9000;\ndisplay: flex; background: rgba(255,255,255,.97); backdrop-filter: blur(14px);\nborder-bottom: 1px solid rgba(0,0,0,.08); box-shadow: 0 6px 24px rgba(0,0,0,.08);\n}"
new_css = ".tab-bar {\nposition: sticky; top: 0; z-index: 9000;\ndisplay: flex; background: rgba(255,255,255,.82);\nbackdrop-filter: blur(18px) saturate(1.5); -webkit-backdrop-filter: blur(18px) saturate(1.5);\nborder-bottom: 1px solid rgba(0,0,0,.06); box-shadow: 0 4px 20px rgba(0,0,0,.07);\npadding-top: env(safe-area-inset-top, 0px);\n}"
assert old_css in c, 'CSS-bar'
c = c.replace(old_css, new_css, 1)

old_item = ".tab-item {\nflex: 1; min-width: 0; padding: 8px 2px 7px; text-align: center; cursor: pointer;\ncolor: #9ca3af; transition: color .2s ease; -webkit-tap-highlight-color: transparent;\n}"
new_item = ".tab-item {\nflex: 1; min-width: 0; padding: 7px 2px 8px; text-align: center; cursor: pointer; position: relative;\ncolor: #9aa1ab; transition: color .25s ease; -webkit-tap-highlight-color: transparent; user-select: none;\n}\n.tab-item:active { transform: scale(.9); }"
assert old_item in c, 'CSS-item'
c = c.replace(old_item, new_item, 1)

old_ico = ".tab-item .tab-ico { font-size: 21px; line-height: 1.2; display: block; }"
new_ico = ".tab-item .tab-ico { font-size: 20px; line-height: 1.2; display: block; transition: transform .35s cubic-bezier(.34,1.56,.64,1); filter: grayscale(.35); opacity: .8; }\n.tab-item .tab-glow { position: absolute; left: 50%; top: 4px; transform: translateX(-50%); width: 44px; height: 26px; border-radius: 999px; background: linear-gradient(135deg, rgba(14,124,102,.16), rgba(6,182,212,.10)); opacity: 0; transition: opacity .3s ease; pointer-events: none; }"
assert old_ico in c, 'CSS-ico'
c = c.replace(old_ico, new_ico, 1)

old_act = ".tab-item.active { color: var(--accent, #0E7C66); }\n.tab-item.active .tab-ico { transform: translateY(-1px); }"
new_act = ".tab-item.active { color: var(--accent, #0E7C66); }\n.tab-item.active .tab-ico { transform: translateY(-1px) scale(1.1); filter: none; opacity: 1; }\n.tab-item.active .tab-lbl { font-weight: 700; }\n.tab-item.active .tab-glow { opacity: 1; }\n.tab-badge { position: absolute; top: 3px; right: calc(50% - 20px); min-width: 9px; height: 9px; border-radius: 999px; background: #ff4757; border: 2px solid #fff; display: none; box-shadow: 0 1px 5px rgba(255,71,87,.55); }\n.tab-badge.show { display: block; animation: badgePop .45s cubic-bezier(.34,1.56,.64,1); }\n@keyframes badgePop { from { transform: scale(0); } to { transform: scale(1); } }"
assert old_act in c, 'CSS-act'
c = c.replace(old_act, new_act, 1)
print('CSS 已替换')

# ===== 2. HTML 加 glow/badge =====
items = {
    'data-tab="journey"><span class="tab-ico"': 'data-tab="journey"><span class="tab-glow"></span><span class="tab-ico"',
    'data-tab="photos"><span class="tab-ico"': 'data-tab="photos"><span class="tab-glow"></span><span class="tab-ico"',
    'data-tab="story"><span class="tab-ico"': 'data-tab="story"><span class="tab-glow"></span><span class="tab-ico"',
    'data-tab="quiz"><span class="tab-ico"': 'data-tab="quiz"><span class="tab-glow"></span><span class="tab-ico"',
    'data-tab="ach"><span class="tab-ico"': 'data-tab="ach"><span class="tab-glow"></span><span class="tab-ico"',
    'data-tab="mine"><span class="tab-ico"': 'data-tab="mine"><span class="tab-glow"></span><span class="tab-badge" id="mineBadge"></span><span class="tab-ico"',
}
for k, v in items.items():
    assert k in c, 'HTML-' + k[:20]
    c = c.replace(k, v, 1)
print('HTML 已更新')

# ===== 3. JS 今日来信标记 =====
anchor = "          if (lv2) liveHtml = '"
i = c.find(anchor)
assert i > 0, 'lv2锚点'
insert = "          if (lv2) { try { window._hasNewLetter = true; } catch(e) {} }\n"
c = c[:i] + insert + c[i:]
print('今日来信标记已加')

# ===== 4. JS 渲染后红点 =====
old_render = "      letterList.innerHTML = html;"
assert old_render in c, 'render锚点'
c = c.replace(old_render, old_render + "\n      try {\n        if (window._hasNewLetter) { var mb = document.getElementById('mineBadge'); if (mb) mb.classList.add('show'); }\n      } catch(e) {}", 1)
print('红点显示已加')

# ===== 5. JS 进入我的消除红点 =====
old_show = "    window.scrollTo(0, 0);"
new_show = "    if (name === 'mine') { var _mb = document.getElementById('mineBadge'); if (_mb) _mb.classList.remove('show'); }\n    window.scrollTo(0, 0);"
assert old_show in c, 'show锚点'
c = c.replace(old_show, new_show, 1)
print('红点消除已加')

assert c != orig
open(P, 'w', encoding='utf-8', newline='\n').write(c)
print('全部完成')
