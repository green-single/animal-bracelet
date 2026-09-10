# -*- coding: utf-8 -*-
"""动物页体验升级：favicon + 首屏Loading + Tab淡入淡出 + CSS瘦身"""
import sys, re, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')
P = 'app/static/animal.html'
c = open(P, encoding='utf-8', newline='').read()
crlf = '\r\n' in c
c = c.replace('\r\n', '\n')
orig = len(c)

# ---------- 1. favicon ----------
svg = "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'><rect width='64' height='64' rx='14' fill='#1b4332'/><circle cx='32' cy='32' r='22' fill='none' stroke='#40916c' stroke-width='3'/><circle cx='32' cy='32' r='13' fill='none' stroke='#74c69d' stroke-width='3'/><circle cx='32' cy='32' r='5' fill='#d8f3dc'/><path d='M32 32 L45 18' stroke='#d8f3dc' stroke-width='3' stroke-linecap='round'/></svg>"
enc = urllib.parse.quote(svg, safe='')
fav_tag = '<link rel="icon" href="data:image/svg+xml,%s">' % enc
if 'rel="icon"' not in c:
    c = c.replace('<meta charset="UTF-8">', '<meta charset="UTF-8">\n  ' + fav_tag, 1)
    print('1. favicon 已加')

# ---------- 2. Loading CSS + HTML + JS ----------
load_css = """
  #pageLoader{position:fixed;inset:0;z-index:99999;display:flex;flex-direction:column;align-items:center;justify-content:center;background:radial-gradient(circle at 50% 38%,#14532d,#0b2e1d);transition:opacity .6s ease}
  #pageLoader.pl-done{opacity:0;pointer-events:none}
  .pl-radar{width:120px;height:120px;position:relative;display:flex;align-items:center;justify-content:center}
  .pl-radar span{position:absolute;inset:0;border:2px solid rgba(116,198,157,.55);border-radius:50%;animation:plRipple 2s ease-out infinite}
  .pl-radar span:nth-child(2){animation-delay:.7s}
  .pl-radar span:nth-child(3){animation-delay:1.4s}
  .pl-radar i{width:12px;height:12px;border-radius:50%;background:#d8f3dc;box-shadow:0 0 20px #74c69d;position:relative;z-index:2;animation:plPulse 1.2s ease-in-out infinite}
  .pl-text{margin-top:24px;color:#a7d7c4;font-size:15px;letter-spacing:3px;animation:plText 1.6s ease-in-out infinite}
  @keyframes plRipple{0%{transform:scale(.35);opacity:.9}100%{transform:scale(1);opacity:0}}
  @keyframes plPulse{0%,100%{transform:scale(1)}50%{transform:scale(1.35)}}
  @keyframes plText{0%,100%{opacity:.55}50%{opacity:1}}
"""
if '#pageLoader' not in c:
    i = c.find('<style>')
    assert i >= 0, 'style块未找到'
    c = c[:i+7] + load_css + c[i+7:]
    print('2a. Loading CSS 已加')

load_html = '\n  <div id="pageLoader"><div class="pl-radar"><span></span><span></span><span></span><i></i></div><div class="pl-text">正在追踪它的位置…</div></div>'
if 'id="pageLoader"' not in c:
    c = c.replace('<body>', '<body>' + load_html, 1)
    print('2b. Loading HTML 已加')

load_js = """
  function hidePageLoader() {
    var el = document.getElementById('pageLoader');
    if (!el) return;
    el.classList.add('pl-done');
    setTimeout(function() { if (el.parentNode) el.parentNode.removeChild(el); }, 700);
  }
"""
if 'function hidePageLoader' not in c:
    # 在 _runAbcd 调用后加
    anchor = "try { window._runAbcd(); } catch(e) { console.log('abcd err', e); }"
    assert anchor in c, '_runAbcd调用点未找到'
    c = c.replace(anchor, anchor + "\n      hidePageLoader();", 1)
    # 函数定义加在第一个 <script> 后
    j = c.find('<script>')
    assert j >= 0, 'script块未找到'
    c = c[:j+8] + '\n' + load_js + c[j+8:]
    print('2c. Loading JS 已加(含 _runAbcd 后触发)')

# ---------- 3. Tab 淡入淡出 ----------
old_holder = "    if (holder) holder.classList.add('active');"
new_holder = "    if (holder) { holder.classList.add('active'); holder.classList.remove('tab-fade'); void holder.offsetWidth; holder.classList.add('tab-fade'); }"
if old_holder in c:
    c = c.replace(old_holder, new_holder, 1)
    fade_css = "\n  .tab-fade{animation:tabFade .45s ease}\n  @keyframes tabFade{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}\n"
    if '.tab-fade' not in c:
        i = c.find('</style>')
        assert i >= 0
        c = c[:i] + fade_css + c[i:]
        print('3. Tab淡入淡出 已加')
else:
    print('3. WARN: showTab锚点未找到')

# ---------- 4. CSS 瘦身（style块：去注释+去缩进+去空行） ----------
def minify_css(m):
    s = m.group(1)
    s = re.sub(r'/\*.*?\*/', '', s, flags=re.S)   # 去注释
    lines = [l.strip() for l in s.split('\n')]
    s = '\n'.join(l for l in lines if l)          # 去空行+缩进
    return '<style>' + s + '</style>'

before = len(c)
c = re.sub(r'<style>(.*?)</style>', minify_css, c, count=1, flags=re.S)
after = len(c)
print(f'4. CSS瘦身: {before//1024}KB → {after//1024}KB (减{(before-after)//1024}KB)')

# ---------- 写回 ----------
open(P, 'w', encoding='utf-8', newline='\n').write(c)
print(f'总大小: {orig//1024}KB → {len(c)//1024}KB | 原CRLF:{crlf} → LF')
