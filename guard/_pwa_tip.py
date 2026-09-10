# -*- coding: utf-8 -*-
"""手机端优化 + PWA添加到主屏幕引导条"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

PWA_TIP_CSS = """
/* PWA 添加到主屏幕引导 */
#pwaTip{display:none;margin:10px 14px 0;padding:12px 14px;border-radius:14px;background:linear-gradient(135deg,rgba(18,121,111,.12),rgba(18,121,111,.2));border:1px solid rgba(18,121,111,.3);font-size:12.5px;color:#0A5C4C;line-height:1.6;position:relative}
#pwaTip b{color:#0E7C66}
#pwaTip .pwa-x{position:absolute;top:8px;right:10px;border:none;background:transparent;font-size:14px;color:#0A5C4C;cursor:pointer;padding:4px}
"""

PWA_TIP_HTML = """<div id="pwaTip"><b>📲 把它装到桌面</b>，以后像 App 一样一键打开<br><span id="pwaTipHow"></span><button class="pwa-x" onclick="dismissPwaTip()">✕</button></div>"""

PWA_TIP_JS = """
(function(){
  try{
    if(localStorage.getItem('pwaTipDismissed')) return;
    var ua = navigator.userAgent;
    var isIOS = /iphone|ipad|ipod/i.test(ua);
    var isAndroid = /android/i.test(ua);
    if(!isIOS && !isAndroid) return;
    var el = document.getElementById('pwaTip');
    if(!el) return;
    var how = document.getElementById('pwaTipHow');
    if(how) how.innerHTML = isIOS
      ? '点浏览器底部 <b>分享按钮</b> → <b>添加到主屏幕</b>'
      : '点浏览器右上角 <b>⋮</b> → <b>安装应用 / 添加到主屏幕</b>';
    el.style.display = 'block';
    window.dismissPwaTip = function(){ el.style.display='none'; try{localStorage.setItem('pwaTipDismissed','1');}catch(e){} };
  }catch(e){}
})();
"""

# ---------- animal.html ----------
P = 'app/static/animal.html'
c = open(P, encoding='utf-8', newline='').read()
c = c.replace('\r\n', '\n')

# 1. CSS：加引导条样式 + 手机端 header 精简
css_anchor = '@media (max-width: 560px) {'
assert css_anchor in c, 'animal media 锚点未找到'
mobile_add = """@media (max-width: 560px) {
/* 手机端：header 精简 */
header { padding: 10px 12px; gap: 8px; }
.code-search input { display: none; }
.brand { font-size: 14px; }
.brand small { font-size: 10px; }
.code-search button { padding: 8px 11px; font-size: 12px; border-radius: 10px; }
/* 地图头部信息更大更透气 */
.map-head { padding: 14px 14px 10px; gap: 10px; }
.map-head .avatar { width: 50px; height: 50px; }
.map-head .t { font-size: 18px; }
.map-head .s { font-size: 12px; }
.view-btns { gap: 5px; }
.view-btn { padding: 7px 11px; font-size: 11.5px; }
#map { height: 380px; }
"""
c = c.replace(css_anchor, mobile_add, 1)

# 2. 引导条 CSS（插到 style 末尾前——用 </style> 锚点）
style_end = '</style>'
assert style_end in c
c = c.replace(style_end, PWA_TIP_CSS + '\n' + style_end, 1)

# 3. 引导条 HTML（header 后、main 前）
header_end = '</header>\n\n<main>'
assert header_end in c
c = c.replace(header_end, '</header>\n' + PWA_TIP_HTML + '\n<main>', 1)

# 4. JS（插到 </body> 前）
body_end = '</body>'
assert body_end in c
c = c.replace(body_end, PWA_TIP_JS + '\n' + body_end, 1)
open(P, 'w', encoding='utf-8', newline='\n').write(c)
print('animal.html 已优化')

# ---------- index.html ----------
P2 = 'app/static/index.html'
c2 = open(P2, encoding='utf-8', newline='').read()
c2 = c2.replace('\r\n', '\n')
# CSS
style_end2 = '</style>'
assert style_end2 in c2
c2 = c2.replace(style_end2, PWA_TIP_CSS + '\n' + style_end2, 1)
# HTML：header 后
header_end2 = '</header>\n\n<main>'
assert header_end2 in c2
c2 = c2.replace(header_end2, '</header>\n' + PWA_TIP_HTML + '\n<main>', 1)
# JS
body_end2 = '</body>'
assert body_end2 in c2
c2 = c2.replace(body_end2, PWA_TIP_JS + '\n' + body_end2, 1)
open(P2, 'w', encoding='utf-8', newline='\n').write(c2)
print('index.html 已加引导条')
