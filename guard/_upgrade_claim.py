# -*- coding: utf-8 -*-
"""领养仪式升级：证书精致化（头像+迷你轨迹+守护契约印章动画）
行级处理（CRLF安全）
"""
P = 'app/static/claim.html'
NL = chr(10)
c = open(P, encoding='utf-8').read()
lines = c.split(NL)

# ---------- 1. CSS：证书升级样式 ----------
css_add = """
  /* ---------- 领养证书 · 升级版 ---------- */
  .certificate {
    width: 100%; max-width: 380px;
    background:
      radial-gradient(ellipse at 50% 0%, rgba(245,158,11,0.08), transparent 60%),
      linear-gradient(160deg, #1C2230 0%, #141920 60%, #12161D 100%);
    border: 2px solid rgba(245,158,11,0.6);
    border-radius: 26px; padding: 36px 26px 30px;
    position: relative; overflow: hidden; margin-top: 28px;
    box-shadow: 0 24px 70px rgba(0,0,0,0.55), 0 0 60px rgba(245,158,11,0.12),
                inset 0 0 60px rgba(245,158,11,0.03);
    opacity: 0; transform: scale(0.6) translateY(30px);
    transition: opacity .5s ease, transform .6s cubic-bezier(.34,1.56,.64,1);
  }
  .certificate.show { opacity: 1; transform: scale(1) translateY(0); }
  .certificate::before {
    content: ''; position: absolute; top: 8px; left: 8px; right: 8px; bottom: 8px;
    border: 1px solid rgba(245,158,11,0.25); border-radius: 20px;
    pointer-events: none;
  }
  .certificate::after {
    content: ''; position: absolute; inset: 0; pointer-events: none;
    background:
      linear-gradient(90deg, transparent 48%, rgba(255,255,255,0.03) 50%, transparent 52%),
      linear-gradient(0deg, transparent 48%, rgba(255,255,255,0.02) 50%, transparent 52%);
    background-size: 24px 24px;
  }
  .cert-vow {
    font-size: 12px; color: var(--gold); letter-spacing: .5em;
    text-align: center; text-transform: uppercase;
    font-weight: 600; position: relative; z-index: 1;
  }
  .cert-vow-en {
    font-size: 9px; color: rgba(245,158,11,0.5); letter-spacing: .3em;
    text-align: center; text-transform: uppercase; margin-top: 4px;
    position: relative; z-index: 1;
  }
  .cert-avatar {
    width: 92px; height: 92px; border-radius: 50%; margin: 22px auto 0;
    border: 3px solid rgba(245,158,11,0.7); overflow: hidden;
    box-shadow: 0 0 30px rgba(245,158,11,0.25), 0 8px 24px rgba(0,0,0,0.4);
    position: relative; z-index: 1;
    background: linear-gradient(145deg, #2A3242, #1A2030);
  }
  .cert-avatar img { width: 100%; height: 100%; object-fit: cover; display: block; }
  .cert-avatar-ring {
    position: absolute; width: 108px; height: 108px; border-radius: 50%;
    border: 1px dashed rgba(245,158,11,0.35);
    left: 50%; transform: translateX(-50%);
    margin-top: 14px; z-index: 0;
    animation: certRingSpin 24s linear infinite;
  }
  @keyframes certRingSpin { from { transform: translateX(-50%) rotate(0); } to { transform: translateX(-50%) rotate(360deg); } }
  .cert-animal {
    font-size: 28px; font-weight: 800; text-align: center;
    margin-top: 18px; color: var(--ink); position: relative; z-index: 1;
    letter-spacing: .04em;
  }
  .cert-nickname {
    font-size: 14px; color: var(--accent); text-align: center;
    margin-top: 8px; font-weight: 600; position: relative; z-index: 1;
  }
  .cert-track {
    display: block; width: 220px; height: 56px; margin: 16px auto 0;
    position: relative; z-index: 1;
  }
  .cert-track .track-bg { stroke: rgba(255,255,255,0.08); stroke-width: 2; fill: none; stroke-dasharray: 3 5; }
  .cert-track .track-main { stroke: var(--accent); stroke-width: 2.5; fill: none; stroke-linecap: round; }
  .cert-track .track-start { fill: var(--accent2); }
  .cert-track .track-end { fill: var(--gold); }
  .cert-divider {
    width: 70px; height: 2px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
    margin: 18px auto; position: relative; z-index: 1;
  }
  .cert-info { position: relative; z-index: 1; }
  .cert-seal {
    width: 70px; height: 70px; border-radius: 50%;
    border: 3px solid rgba(245,158,11,0.8);
    display: flex; align-items: center; justify-content: center;
    font-size: 30px; margin: 22px auto 0;
    background: radial-gradient(circle, rgba(245,158,11,0.18), rgba(245,158,11,0.05));
    box-shadow: 0 0 24px rgba(245,158,11,0.25);
    position: relative; z-index: 1;
    transform: scale(0) rotate(-40deg);
    transition: transform .5s cubic-bezier(.34,1.56,.64,1);
  }
  .certificate.show .cert-seal { transform: scale(1) rotate(0); transition-delay: .5s; }
  .cert-seal::after {
    content: ''; position: absolute; inset: 5px; border-radius: 50%;
    border: 1px dashed rgba(245,158,11,0.4);
    animation: sealSpin 12s linear infinite;
  }
  @keyframes sealSpin { from { transform: rotate(0); } to { transform: rotate(360deg); } }
  .cert-glow {
    position: absolute; top: 50%; left: 50%; width: 0; height: 0;
    border-radius: 50%; transform: translate(-50%, -50%);
    background: radial-gradient(circle, rgba(245,158,11,0.5), transparent 65%);
    transition: width 1.2s ease, height 1.2s ease, opacity 1.2s ease;
    opacity: 0; z-index: 0;
  }
  .certificate.show .cert-glow { width: 480px; height: 480px; opacity: .5; }
"""

# 插入到 .already-claimed 样式前（错误状态样式后）
anchor_css = '  /* ---------- 已领养状态 ---------- */'
idx = None
for i, l in enumerate(lines):
    if anchor_css in l:
        idx = i
        break
assert idx is not None, 'CSS锚点未找到'
# 保持缩进（css_add首行无缩进，改为2空格）
css_lines = css_add.strip(NL).split(NL)
for j, l in enumerate(css_lines):
    if l.strip():
        css_lines[j] = '  ' + l
lines[idx:idx] = css_lines

# ---------- 2. HTML：证书结构升级 ----------
old_cert = [
    '  <div class="certificate" id="certificate">',
    '    <div class="cert-title">Adoption Certificate</div>',
    '    <div class="cert-animal" id="certAnimal">—</div>',
    '    <div class="cert-nickname" id="certNickname"></div>',
    '    <div class="cert-divider"></div>',
    '    <div class="cert-info">',
    '      <div>领养日期：<b id="certDate">—</b></div>',
    '      <div>追踪编号：<b id="certCode">—</b></div>',
    '      <div>数据来源：<b>Movebank 公开科研数据</b></div>',
    '    </div>',
    '    <div class="cert-seal">🐾</div>',
    '  </div>',
]
new_cert = [
    '  <div class="certificate" id="certificate">',
    '    <div class="cert-glow" id="certGlow"></div>',
    '    <div class="cert-vow">守护契约</div>',
    '    <div class="cert-vow-en">Guardianship Vow</div>',
    '    <div class="cert-avatar-ring"></div>',
    '    <div class="cert-avatar"><img id="certAvatar" alt="" src=""></div>',
    '    <div class="cert-animal" id="certAnimal">—</div>',
    '    <div class="cert-nickname" id="certNickname"></div>',
    '    <svg class="cert-track" viewBox="0 0 220 56" id="certTrack">',
    '      <path class="track-bg" d="M12 44 Q 55 8, 100 30 T 208 18" />',
    '      <path class="track-main" d="M12 44 Q 55 8, 100 30 T 208 18" />',
    '      <circle class="track-start" cx="12" cy="44" r="4" />',
    '      <circle class="track-end" cx="208" cy="18" r="4" />',
    '    </svg>',
    '    <div class="cert-divider"></div>',
    '    <div class="cert-info">',
    '      <div>领养日期：<b id="certDate">—</b></div>',
    '      <div>追踪编号：<b id="certCode">—</b></div>',
    '      <div>守护者：<b id="certGuardian">—</b></div>',
    '      <div>数据来源：<b>Movebank 公开科研数据</b></div>',
    '    </div>',
    '    <div class="cert-seal">🐾</div>',
    '  </div>',
]
# 找证书块起止
start_idx = None
for i, l in enumerate(lines):
    if 'id="certificate"' in l:
        start_idx = i
        break
assert start_idx is not None, '证书块未找到'
end_idx = None
for i in range(start_idx, start_idx + 20):
    if lines[i].strip() == '</div>' and i > start_idx:
        # 证书块结束：certificate的闭合div（在cert-seal之后）
        end_idx = i
        break
assert end_idx is not None, '证书结束未找到'
# 校验old_cert匹配
actual = lines[start_idx:end_idx + 1]
for o, a in zip(old_cert, actual):
    assert o.strip() == a.strip(), '证书内容不匹配: %r vs %r' % (o, a)
lines[start_idx:end_idx + 1] = new_cert

# ---------- 3. JS：领养成功后填充头像+守护者+动画 ----------
old_js = [
    "              // 填充证书",
    "              document.getElementById('certAnimal').textContent = animalData.name;",
    "              document.getElementById('certNickname').textContent = nickname ? ('昵称：' + nickname) : '';",
    "              document.getElementById('certDate').textContent = new Date().toLocaleDateString('zh-CN');",
    "              document.getElementById('certCode').textContent = code;",
]
new_js = [
    "              // 填充证书（升级版）",
    "              document.getElementById('certAnimal').textContent = animalData.name;",
    "              document.getElementById('certNickname').textContent = nickname ? ('昵称：' + nickname) : '';",
    "              document.getElementById('certGuardian').textContent = nickname ? (nickname + ' 的守护者') : '无名守护者';",
    "              document.getElementById('certDate').textContent = new Date().toLocaleDateString('zh-CN');",
    "              document.getElementById('certCode').textContent = code;",
    "              var certImg = document.getElementById('certAvatar');",
    "              if (firstPhoto && certImg) { certImg.src = firstPhoto; }",
]
# 找old_js起始
for i in range(len(lines) - len(old_js)):
    if all(lines[i + k].strip() == old_js[k].strip() for k in range(len(old_js))):
        lines[i:i + len(old_js)] = new_js
        break
else:
    raise AssertionError('JS填充块未找到')

# ---------- 4. JS：证书展开动画（showStage('stageCelebrate')后加延时） ----------
old_show = "              createConfetti();\n              showStage('stageCelebrate');"
# 行级
old_show_lines = ["              createConfetti();", "              showStage('stageCelebrate');"]
new_show_lines = [
    "              createConfetti();",
    "              showStage('stageCelebrate');",
    "              // 证书展开动画：先光芒，再证书，最后印章",
    "              setTimeout(function () {",
    "                var cert = document.getElementById('certificate');",
    "                if (cert) cert.classList.add('show');",
    "              }, 600);",
]
for i in range(len(lines) - 1):
    if lines[i].strip() == old_show_lines[0].strip() and lines[i + 1].strip() == old_show_lines[1].strip():
        lines[i:i + 2] = new_show_lines
        break
else:
    raise AssertionError('showStage庆祝锚点未找到')

c = NL.join(lines)
open(P, 'w', encoding='utf-8').write(c)
print('OK 领养仪式升级完成')
print('守护契约:', c.count('cert-vow'))
print('头像:', c.count('certAvatar'))
print('守护者:', c.count('certGuardian'))
print('展开动画:', c.count("cert.classList.add('show')"))
