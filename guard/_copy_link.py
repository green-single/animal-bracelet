# -*- coding: utf-8 -*-
"""pwaTip 微信分支：加复制链接按钮"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

NEW_JS = """
<script>
(function(){
  function copyText(txt){
    try{
      if(navigator.clipboard && navigator.clipboard.writeText){
        return navigator.clipboard.writeText(txt).then(function(){return true;}).catch(function(){return false;});
      }
      // 降级
      var ta = document.createElement('textarea');
      ta.value = txt; ta.style.position = 'fixed'; ta.style.opacity = '0';
      document.body.appendChild(ta); ta.select();
      try{ document.execCommand('copy'); }catch(e){}
      document.body.removeChild(ta);
      return Promise.resolve(true);
    }catch(e){ return Promise.resolve(false); }
  }
  try{
    var ua = navigator.userAgent;
    var isWechat = /MicroMessenger/i.test(ua);
    if (window.matchMedia && window.matchMedia('(display-mode: standalone)').matches) return;
    if (localStorage.getItem('pwaTipDismissed')) return;
    var isIOS = /iphone|ipad|ipod/i.test(ua);
    var isAndroid = /android/i.test(ua);
    if(!isIOS && !isAndroid) return;
    var el = document.getElementById('pwaTip');
    if(!el) return;
    var how = document.getElementById('pwaTipHow');
    if(how){
      if(isWechat){
        how.innerHTML = '微信里不能装到桌面：<b>点右上角 ⋯ → 在浏览器打开</b>，然后在浏览器里 <b>添加到主屏幕</b><br><span id="copyLinkTip" style="font-size:11px;color:#8a6d1d;">或点下面按钮复制链接，粘贴到浏览器打开</span>';
      } else if(isIOS){
        how.innerHTML = '点浏览器底部 <b>分享按钮</b> → <b>添加到主屏幕</b>';
      } else {
        how.innerHTML = '点浏览器右上角 <b>⋮</b> → <b>安装应用 / 添加到主屏幕</b>';
      }
    }
    el.style.display = 'block';
    if(isWechat){
      var cp = document.getElementById('copyLinkBtn');
      if(!cp){
        cp = document.createElement('button');
        cp.id = 'copyLinkBtn';
        cp.textContent = '📋 复制链接到浏览器打开';
        cp.style.cssText = 'margin-top:8px;padding:8px 14px;border:none;border-radius:10px;background:#fff;color:#0E7C66;font-size:12px;font-weight:700;cursor:pointer;';
        el.appendChild(cp);
        cp.addEventListener('click', function(){
          var url = location.href;
          copyText(url).then(function(ok){
            cp.textContent = ok ? '✅ 已复制，去浏览器粘贴打开' : '复制失败，请手动复制地址栏链接';
            setTimeout(function(){ cp.textContent = '📋 复制链接到浏览器打开'; }, 3000);
          });
        });
      }
    }
    window.dismissPwaTip = function(){ el.style.display='none'; try{localStorage.setItem('pwaTipDismissed','1');}catch(e){} };
  }catch(e){}
})();
</script>
"""

def replace_js(page):
    c = open(page, encoding='utf-8', newline='').read()
    c = c.replace('\r\n', '\n')
    # 找 pwaTip JS 块：从 '<script>\n(function(){' 到 '</script>'（含 pwaTipDismissed 的块）
    idx = c.find('pwaTipDismissed')
    if idx == -1:
        print(page, '未找到旧JS')
        return
    start = c.rfind('<script>', 0, idx)
    end = c.find('</script>', idx) + len('</script>')
    c = c[:start] + NEW_JS + c[end:]
    open(page, 'w', encoding='utf-8', newline='\n').write(c)
    print(page, 'JS已更新')

for p in ['app/static/animal.html', 'app/static/index.html']:
    replace_js(p)
print('完成')
