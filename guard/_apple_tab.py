# -*- coding: utf-8 -*-
"""苹果风改造：
1. tab-bar 悬浮圆角胶囊（sticky 顶部，苹果照片app风格）
2. header 取消 sticky（滚动让位，避免双栏重叠）
3. 手机端顶部行精简（隐藏查询按钮+brand小字）
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

P = 'app/static/animal.html'
c = open(P, encoding='utf-8', newline='').read()
c = c.replace('\r\n', '\n')
orig = c

# ===== 1. header 取消 sticky =====
old_h = """header {
display: flex; align-items: center; gap: 10px; padding: 14px 18px;
position: sticky; top: 0; background: rgba(244,243,238,0.9); backdrop-filter: blur(8px);
z-index: 1000; border-bottom: 1px solid var(--line);
}"""
new_h = """header {
display: flex; align-items: center; gap: 10px; padding: 14px 18px 6px;
background: transparent; border-bottom: none;
}"""
assert old_h in c, 'header锚点'
c = c.replace(old_h, new_h, 1)
print('header 已去 sticky')

# ===== 2. tab-bar 圆角胶囊 =====
old_tab = """.tab-bar {
position: sticky; top: 0; z-index: 9000;
display: flex; background: rgba(255,255,255,.82);
backdrop-filter: blur(18px) saturate(1.5); -webkit-backdrop-filter: blur(18px) saturate(1.5);
border-bottom: 1px solid rgba(0,0,0,.06); box-shadow: 0 4px 20px rgba(0,0,0,.07);
padding-top: env(safe-area-inset-top, 0px);
}"""
new_tab = """.tab-bar {
position: sticky; top: calc(env(safe-area-inset-top, 0px) + 8px); z-index: 9000;
display: flex; margin: 8px 12px 4px;
background: rgba(255,255,255,.82);
backdrop-filter: blur(18px) saturate(1.5); -webkit-backdrop-filter: blur(18px) saturate(1.5);
border-radius: 26px; border: 1px solid rgba(255,255,255,.7);
box-shadow: 0 6px 24px rgba(0,0,0,.10), inset 0 0 0 .5px rgba(0,0,0,.04);
overflow: hidden;
}"""
assert old_tab in c, 'tabbar锚点'
c = c.replace(old_tab, new_tab, 1)
print('tab-bar 已改圆角胶囊')

# ===== 3. 手机端顶部行精简 =====
old_m = """.code-search button { padding: 8px 11px; font-size: 12px; border-radius: 10px; }"""
new_m = """.code-search button { padding: 8px 11px; font-size: 12px; border-radius: 10px; }
.code-search #codeGo { display: none; }
.brand { font-size: 13px; }
.brand small { display: none; }"""
assert old_m in c, 'media锚点'
c = c.replace(old_m, new_m, 1)
print('手机端顶部精简已加')

assert c != orig
open(P, 'w', encoding='utf-8', newline='\n').write(c)
print('全部完成')
