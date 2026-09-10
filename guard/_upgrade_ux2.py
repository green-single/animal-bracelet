# -*- coding: utf-8 -*-
"""主页+领养页+后台：favicon + 主页Loading"""
import sys, re, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')

svg = "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'><rect width='64' height='64' rx='14' fill='#1b4332'/><circle cx='32' cy='32' r='22' fill='none' stroke='#40916c' stroke-width='3'/><circle cx='32' cy='32' r='13' fill='none' stroke='#74c69d' stroke-width='3'/><circle cx='32' cy='32' r='5' fill='#d8f3dc'/><path d='M32 32 L45 18' stroke='#d8f3dc' stroke-width='3' stroke-linecap='round'/></svg>"
enc = urllib.parse.quote(svg, safe='')
fav_tag = '<link rel="icon" href="data:image/svg+xml,%s">' % enc

LOAD_CSS = """
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
LOAD_HTML = '\n  <div id="pageLoader"><div class="pl-radar"><span></span><span></span><span></span><i></i></div><div class="pl-text">正在追踪它的位置…</div></div>'

def add_fav(c):
    if 'rel="icon"' not in c:
        c = c.replace('<meta charset="UTF-8">', '<meta charset="UTF-8">\n  ' + fav_tag, 1)
    return c

def add_loading(c, hide_js):
    if '#pageLoader' not in c:
        i = c.find('<style>')
        if i >= 0:
            c = c[:i+7] + LOAD_CSS + c[i+7:]
        else:
            # 无style块：加到head
            i = c.find('</head>')
            c = c[:i] + '<style>' + LOAD_CSS + '</style>\n' + c[i:]
    if 'id="pageLoader"' not in c:
        c = c.replace('<body>', '<body>' + LOAD_HTML, 1)
    if 'function hidePageLoader' not in c:
        c = c.replace('</body>', '<script>' + hide_js + '</script>\n</body>', 1)
    return c

HIDE_JS = """
function hidePageLoader(){var el=document.getElementById('pageLoader');if(!el)return;el.classList.add('pl-done');setTimeout(function(){if(el.parentNode)el.parentNode.removeChild(el);},700);}
window.addEventListener('load', function(){ setTimeout(hidePageLoader, 300); });
setTimeout(hidePageLoader, 5000); // 兜底
"""

for f, do_load in [('app/static/index.html', True), ('app/static/claim.html', False), ('app/static/admin.html', True)]:
    c = open(f, encoding='utf-8', newline='').read()
    crlf = '\r\n' in c
    c = c.replace('\r\n', '\n')
    c = add_fav(c)
    if do_load:
        c = add_loading(c, HIDE_JS)
    open(f, 'w', encoding='utf-8', newline='\n').write(c)
    print(f'{f}: favicon={("rel=\"icon\"" in c)} | loading={("#pageLoader" in c)} | CRLF原:{crlf} → LF | {len(c)//1024}KB')
