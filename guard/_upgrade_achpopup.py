# -*- coding: utf-8 -*-
"""成就解锁弹窗动画：金光光环+徽章弹入+队列"""
P = 'app/static/animal.html'
NL = chr(10)
c = open(P, encoding='utf-8').read()
lines = c.split(NL)

# ---------- 1. CSS：弹窗样式（插在成就系统CSS前） ----------
css_block = [
    "  /* ---------- 成就解锁弹窗 ---------- */",
    "  .ach-popup-overlay {",
    "    position: fixed; inset: 0; z-index: 9999;",
    "    display: flex; align-items: center; justify-content: center;",
    "    background: rgba(5,8,14,0.72);",
    "    opacity: 0; pointer-events: none; transition: opacity .3s ease;",
    "    backdrop-filter: blur(3px);",
    "  }",
    "  .ach-popup-overlay.show { opacity: 1; pointer-events: auto; }",
    "  .ach-popup { text-align: center; transform: scale(.6); transition: transform .45s cubic-bezier(.34,1.56,.64,1); }",
    "  .ach-popup-overlay.show .ach-popup { transform: scale(1); }",
    "  .ach-popup-ring { position: relative; width: 150px; height: 150px; margin: 0 auto; }",
    "  .ach-popup-ring::before, .ach-popup-ring::after {",
    "    content: ''; position: absolute; inset: 0; border-radius: 50%;",
    "    border: 3px solid rgba(245,158,11,.55); animation: achRing 1.3s ease-out infinite;",
    "  }",
    "  .ach-popup-ring::after { animation-delay: .45s; }",
    "  @keyframes achRing { from { transform: scale(.45); opacity: 1; } to { transform: scale(1.65); opacity: 0; } }",
    "  .ach-popup-icon {",
    "    position: absolute; inset: 0; display: flex; align-items: center; justify-content: center;",
    "    font-size: 62px;",
    "    filter: drop-shadow(0 0 26px rgba(245,158,11,.7));",
    "    animation: achBounce .6s cubic-bezier(.34,1.56,.64,1);",
    "  }",
    "  @keyframes achBounce {",
    "    0% { transform: scale(0) rotate(-24deg); }",
    "    60% { transform: scale(1.25) rotate(8deg); }",
    "    100% { transform: scale(1) rotate(0); }",
    "  }",
    "  .ach-popup-title {",
    "    color: #F59E0B; font-size: 15px; letter-spacing: .28em;",
    "    margin-top: 20px; font-weight: 700; text-transform: uppercase;",
    "  }",
    "  .ach-popup-name { color: #fff; font-size: 23px; font-weight: 800; margin-top: 6px; }",
    "  .ach-popup-sub { color: rgba(255,255,255,.55); font-size: 12px; margin-top: 9px; }",
    "  .ach-popup-rays {",
    "    position: absolute; top: 50%; left: 50%; width: 0; height: 0; border-radius: 50%;",
    "    transform: translate(-50%,-50%);",
    "    background: radial-gradient(circle, rgba(245,158,11,.35), transparent 60%);",
    "    transition: width .9s ease, height .9s ease, opacity .9s ease; opacity: 0;",
    "  }",
    "  .ach-popup-overlay.show .ach-popup-rays { width: 460px; height: 460px; opacity: 1; }",
    "",
]
anchor_css = '  /* ---------- 成就徽章系统 ---------- */'
idx = None
for i, l in enumerate(lines):
    if anchor_css in l:
        idx = i
        break
assert idx is not None, 'CSS锚点未找到'
lines[idx:idx] = css_block

# ---------- 2. HTML：弹窗容器（插在升级庆祝遮罩前） ----------
html_block = [
    "  <!-- 成就解锁弹窗 -->",
    "  <div class=\"ach-popup-overlay\" id=\"achPopup\">",
    "    <div class=\"ach-popup-rays\"></div>",
    "    <div class=\"ach-popup\">",
    "      <div class=\"ach-popup-ring\"><div class=\"ach-popup-icon\" id=\"achPopupIcon\">🏅</div></div>",
    "      <div class=\"ach-popup-title\">✨ 成就解锁</div>",
    "      <div class=\"ach-popup-name\" id=\"achPopupName\">—</div>",
    "      <div class=\"ach-popup-sub\">继续陪伴它，解锁更多徽章</div>",
    "    </div>",
    "  </div>",
    "",
]
anchor_html = '  <!-- 升级庆祝遮罩 -->'
idx = None
for i, l in enumerate(lines):
    if anchor_html in l:
        idx = i
        break
assert idx is not None, 'HTML锚点未找到'
lines[idx:idx] = html_block

# ---------- 3. JS：队列+弹窗函数（插在 window._unlockAch 定义前） ----------
js_queue = [
    "          // 成就解锁弹窗队列",
    "          window._achQueue = [];",
    "          window._achShowing = false;",
    "          window._achShowNext = function () {",
    "            if (window._achShowing || !window._achQueue.length) return;",
    "            window._achShowing = true;",
    "            var a = window._achQueue.shift();",
    "            var o = document.getElementById('achPopup');",
    "            if (!o) { window._achShowing = false; return; }",
    "            var ic = document.getElementById('achPopupIcon');",
    "            var nm = document.getElementById('achPopupName');",
    "            if (ic) ic.textContent = a.ico;",
    "            if (nm) nm.textContent = a.name;",
    "            o.classList.add('show');",
    "            setTimeout(function () {",
    "              o.classList.remove('show');",
    "              window._achShowing = false;",
    "              setTimeout(window._achShowNext, 320);",
    "            }, 2900);",
    "          };",
    "",
]
anchor_js = '          window._unlockAch = function(achId, achName) {'
idx = None
for i, l in enumerate(lines):
    if anchor_js in l:
        idx = i
        break
assert idx is not None, 'JS锚点未找到'
lines[idx:idx] = js_queue

# ---------- 4. JS：unlocked后触发弹窗 ----------
old_unlock = [
    "              if (item) {",
    "                item.classList.remove('locked');",
    "                item.classList.add('unlocked');",
    "              }",
]
new_unlock = [
    "              if (item) {",
    "                item.classList.remove('locked');",
    "                item.classList.add('unlocked');",
    "                // 解锁弹窗（队列最多3个）",
    "                try {",
    "                  var ico = item.querySelector('.achievement-icon');",
    "                  var nm = item.querySelector('.achievement-name');",
    "                  window._achQueue.push({ ico: ico ? ico.textContent : '🏅', name: nm ? nm.textContent : (achName || '成就') });",
    "                  if (window._achQueue.length > 3) window._achQueue.splice(0, window._achQueue.length - 3);",
    "                  window._achShowNext();",
    "                } catch(e2) {}",
    "              }",
]
found = False
for i in range(len(lines) - 3):
    if all(lines[i + k].strip() == old_unlock[k].strip() for k in range(len(old_unlock))):
        lines[i:i + len(old_unlock)] = new_unlock
        found = True
        break
assert found, 'unlocked锚点未找到'

c = NL.join(lines)
open(P, 'w', encoding='utf-8').write(c)
print('OK 成就弹窗完成')
print('弹窗CSS:', c.count('ach-popup-overlay'))
print('弹窗HTML:', c.count('achPopupName'))
print('队列:', c.count('_achQueue'))
print('触发点:', c.count('window._achShowNext()'))
