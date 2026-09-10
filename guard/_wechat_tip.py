# -*- coding: utf-8 -*-
"""微信内引导 + standalone检测 + 已领养页添加主屏幕引导"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

# ========== 1. pwaTip JS 增强（微信分支 + standalone 检测） ==========
NEW_JS = """
<script>
(function(){
  try{
    var ua = navigator.userAgent;
    var isWechat = /MicroMessenger/i.test(ua);
    // 已经是"主屏幕App"模式 → 不再提示
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
        how.innerHTML = '微信里不能装到桌面：<b>点右上角 ⋯ → 在浏览器打开</b>，然后在浏览器里 <b>添加到主屏幕</b>（以后不用再扫码）';
      } else if(isIOS){
        how.innerHTML = '点浏览器底部 <b>分享按钮</b> → <b>添加到主屏幕</b>';
      } else {
        how.innerHTML = '点浏览器右上角 <b>⋮</b> → <b>安装应用 / 添加到主屏幕</b>';
      }
    }
    el.style.display = 'block';
    window.dismissPwaTip = function(){ el.style.display='none'; try{localStorage.setItem('pwaTipDismissed','1');}catch(e){} };
  }catch(e){}
})();
</script>
"""

def replace_js(page):
    c = open(page, encoding='utf-8', newline='').read()
    c = c.replace('\r\n', '\n')
    # 找旧的 pwaTip script 块并替换
    start = c.find("<script>\n(function(){\n  try{\n    if(localStorage.getItem('pwaTipDismissed'))")
    if start == -1:
        # 试另一个开头
        start = c.find("<script>\n(function(){\n  try{\n    if(localStorage.getItem('pwaTipDismissed')) return;")
    if start == -1:
        # 通用：找 pwaTip 所在 script
        idx = c.find("pwaTipDismissed")
        if idx == -1:
            print(page, '未找到旧JS，跳过')
            return
        # 向前找 <script>
        start = c.rfind('<script>', 0, idx)
        end = c.find('</script>', idx) + len('</script>')
        c = c[:start] + NEW_JS + c[end:]
        print(page, 'JS已替换(通用定位)')
    else:
        end = c.find('</script>', start) + len('</script>')
        c = c[:start] + NEW_JS + c[end:]
        print(page, 'JS已替换')
    open(page, 'w', encoding='utf-8', newline='\n').write(c)

for p in ['app/static/animal.html', 'app/static/index.html']:
    replace_js(p)

# ========== 2. claim.html 已领养页：加"添加到主屏幕"引导 ==========
P = 'app/static/claim.html'
c = open(P, encoding='utf-8', newline='').read()
c = c.replace('\r\n', '\n')

old_claimed = """    <p>每一只动物只有一条领养码，一人领养后即失效，这是为了保护这份专属感。<br><br>你仍然可以去看看它的故事和旅程。</p>
    <button class="btn" id="viewBtn" style="margin-top:28px;">去看看它 →</button>"""
new_claimed = """    <p>每一只动物只有一条领养码，一人领养后即失效，这是为了保护这份专属感。<br><br>你仍然可以去看看它的故事和旅程。</p>
    <div id="wechatClaimTip" style="display:none;margin-top:18px;padding:12px 14px;border-radius:12px;background:rgba(245,158,11,.12);border:1px solid rgba(245,158,11,.35);font-size:12.5px;color:#B45309;line-height:1.7;text-align:left;">
      📲 想把它装到桌面随时看？<b>点右上角 ⋯ → 在浏览器打开</b>，再在浏览器里添加到主屏幕
    </div>
    <button class="btn" id="viewBtn" style="margin-top:28px;">去看看它 →</button>"""
assert old_claimed in c, 'claimed锚点'
c = c.replace(old_claimed, new_claimed, 1)

# 在 viewBtn 绑定前加微信检测
old_vb = "document.getElementById('viewBtn').addEventListener('click', function() {"
assert old_vb in c
c = c.replace(old_vb, """      try {
        if (/MicroMessenger/i.test(navigator.userAgent)) {
          document.getElementById('wechatClaimTip').style.display = 'block';
        }
      } catch(e) {}
      """ + old_vb, 1)
print('claim已领养页微信引导已加')

open(P, 'w', encoding='utf-8', newline='\n').write(c)
print('完成')
