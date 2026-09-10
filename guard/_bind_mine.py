# -*- coding: utf-8 -*-
"""已领养页：加"这是我的动物，绑定到这台设备"按钮（精确锚点）"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
P = 'app/static/claim.html'
c = open(P, encoding='utf-8', newline='').read()
c = c.replace('\r\n', '\n')

# 1. HTML：在 viewBtn 前插绑定按钮
old_btn = '    <button class="btn" id="viewBtn" style="margin-top:28px;">去看看它 →</button>'
new_btn = """    <div id="mineTip" style="margin-top:16px;padding:13px 15px;border-radius:12px;background:rgba(16,185,129,.08);border:1px solid rgba(16,185,129,.3);font-size:12.5px;color:#065F46;line-height:1.7;text-align:left;">
      如果这条码就是你之前领养的，可以把它<b>绑定到这台设备</b>——之后从主屏幕图标进去就是它
    </div>
    <button class="btn" id="bindMineBtn" style="margin-top:12px;">🐾 这是我的动物，绑定到这台设备</button>
    <button class="btn ghost" id="viewBtn" style="margin-top:10px;">先去看看它 →</button>"""
assert old_btn in c, 'btn锚点'
c = c.replace(old_btn, new_btn, 1)
print('按钮HTML已加')

# 2. JS：整个 claimed 分支替换（加绑定逻辑）
old_js = """      if (res.d.status === 'claimed') {
              try {
        if (/MicroMessenger/i.test(navigator.userAgent)) {
          document.getElementById('wechatClaimTip').style.display = 'block';
        }
      } catch(e) {}
      document.getElementById('viewBtn').addEventListener('click', function() {
          location.href = '/animal/' + animalData.id;
        });
        showStage('stageClaimed');
        return;
      }"""
new_js = """      if (res.d.status === 'claimed') {
        try {
          if (/MicroMessenger/i.test(navigator.userAgent)) {
            var wt = document.getElementById('wechatClaimTip');
            if (wt) wt.style.display = 'block';
          }
        } catch(e) {}
        document.getElementById('viewBtn').addEventListener('click', function() {
          location.href = '/animal/' + animalData.id;
        });
        // 绑定到这台设备：用码作为凭证，写入本机 localStorage
        var bindBtn = document.getElementById('bindMineBtn');
        if (bindBtn) bindBtn.addEventListener('click', function() {
          try {
            localStorage.setItem('adopted_' + animalData.id, JSON.stringify({
              date: new Date().toISOString(),
              code: code,
              nickname: ''
            }));
          } catch(e) {}
          location.href = '/animal/' + animalData.id;
        });
        showStage('stageClaimed');
        return;
      }"""
assert old_js in c, 'js锚点'
c = c.replace(old_js, new_js, 1)
print('绑定JS已加')

open(P, 'w', encoding='utf-8', newline='\n').write(c)
print('完成')
