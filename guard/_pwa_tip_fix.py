# -*- coding: utf-8 -*-
"""修复：PWA引导JS包script标签"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

PWA_TIP_JS = """
<script>
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
</script>
"""

for page in ['app/static/animal.html', 'app/static/index.html']:
    c = open(page, encoding='utf-8', newline='').read()
    c = c.replace('\r\n', '\n')
    # 移除旧的裸 JS（不带 script 包裹的那段）
    old_bare = """(function(){
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
})();"""
    if old_bare in c:
        c = c.replace(old_bare, '', 1)
        print(page, '移除裸JS')
    # 在 </body> 前插带 script 的版本
    body_end = '</body>'
    assert body_end in c, page
    c = c.replace(body_end, PWA_TIP_JS + body_end, 1)
    open(page, 'w', encoding='utf-8', newline='\n').write(c)
    print(page, '已修复')
