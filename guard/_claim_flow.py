# -*- coding: utf-8 -*-
"""领养页首屏优化 + 已绑定自动跳转 + 领养成功自动进入 + 首页绑定跳转（修复版）"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

new_media = """@media (max-width: 480px) {
  /* 首屏紧凑：不用滚动就能领养 */
  .reveal-avatar { width: 112px; height: 112px; }
  .reveal-avatar-ring { width: 126px; height: 126px; }
  .reveal-label { margin-top: 16px; font-size: 10px; }
  .reveal-name { margin-top: 8px; font-size: 34px; }
  .reveal-species { margin-top: 6px; font-size: 13px; }
  .reveal-story { margin-top: 12px; font-size: 12.5px; max-height: 2.6em; overflow: hidden; position: relative; cursor: pointer; line-height: 1.7; }
  .reveal-story.expanded { max-height: none; }
  .reveal-story::after { content: '展开 ▾'; position: absolute; right: 0; bottom: 0; padding-left: 24px;
    background: linear-gradient(90deg, transparent, #0A0E14 55%); color: var(--accent); font-size: 11px; font-style: normal; }
  .reveal-story.expanded::after { content: ''; }
  .nickname-section { margin-top: 14px; }
  .nickname-label { font-size: 11.5px; margin-bottom: 6px; }
  .nickname-input { padding: 11px; font-size: 15px; border-radius: 12px; }
  .nickname-hint { font-size: 10px; }
  .btn { font-size: 14px; padding: 13px 34px; }
  }
"""

# ========== 1. claim.html ==========
P = 'app/static/claim.html'
c = open(P, encoding='utf-8', newline='').read()
c = c.replace('\r\n', '\n')

old_media = '@media (max-width: 480px) {'
if old_media in c:
    c = c.replace(old_media, new_media, 1)
    print('A1 手机端紧凑CSS 已插入')
else:
    anchor = '</style>'
    assert anchor in c
    c = c.replace(anchor, new_media + '\n' + anchor, 1)
    print('A1 CSS 已追加到 style 末尾')

# --- B. story 点击展开 ---
anchor2 = "animalStories[animalData.id] || (animalData.story || '').substring(0, 100);"
assert anchor2 in c, 'anchor2'
c = c.replace(anchor2, anchor2 + """
      document.getElementById('revealStory').addEventListener('click', function() {
        this.classList.toggle('expanded');
      });""", 1)
print('B story点击展开 已加')

# --- C. 已绑定直接跳转 ---
anchor3 = "      animalData = res.d.animal;\n"
assert anchor3 in c, 'anchor3'
c = c.replace(anchor3, anchor3 + """
      // 本设备已领养过 → 直接进入它的页面（不用再领养）
      try {
        if (localStorage.getItem('adopted_' + animalData.id)) {
          location.replace('/animal/' + animalData.id);
          return;
        }
      } catch(e) {}
""", 1)
print('C 已绑定自动跳转 已加')

# --- D. 领养成功：8秒自动进入 ---
anchor4 = "              createConfetti();\n              showStage('stageCelebrate');"
assert anchor4 in c, 'anchor4'
c = c.replace(anchor4, """              createConfetti();
              showStage('stageCelebrate');
              // 8秒后自动进入它的世界
              var sub = document.getElementById('celebrateSub');
              if (sub) {
                var auto = document.createElement('div');
                auto.id = 'autoGo';
                auto.style.cssText = 'margin-top:10px;font-size:12px;color:var(--sub);';
                auto.textContent = '8 秒后自动进入它的世界…';
                sub.appendChild(auto);
              }
              setTimeout(function(){ location.href = '/animal/' + animalData.id; }, 8000);""", 1)
print('D 领养成功自动进入 已加')

open(P, 'w', encoding='utf-8', newline='\n').write(c)
print('claim.html 完成')

# ========== 2. index.html：有绑定 → 直接进动物页 ==========
P2 = 'app/static/index.html'
c2 = open(P2, encoding='utf-8', newline='').read()
c2 = c2.replace('\r\n', '\n')
body_open = '<body>'
assert body_open in c2, 'body'
jump_js = """<script>
(function(){
  try {
    for (var i = 0; i < localStorage.length; i++) {
      var k = localStorage.key(i);
      if (k && k.indexOf('adopted_') === 0) {
        var id = k.slice(8);
        if (id) { location.replace('/animal/' + id); return; }
      }
    }
  } catch(e) {}
})();
</script>"""
c2 = c2.replace(body_open, body_open + '\n' + jump_js, 1)
open(P2, 'w', encoding='utf-8', newline='\n').write(c2)
print('index.html 绑定跳转 完成')
