# -*- coding: utf-8 -*-
"""Cookie 服务端重定向方案：
- main.py / 路由检查 my_animal cookie → 302 到动物页（不依赖JS）
- claim POST 成功种 cookie
- 前端各处绑定后种 cookie 兜底
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

# ========== 1. main.py ==========
P = 'app/main.py'
c = open(P, encoding='utf-8', newline='').read()
c = c.replace('\r\n', '\n')

# 1.1 JSONResponse import
old_imp = 'from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse'
assert old_imp in c
c = c.replace(old_imp, 'from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse', 1)
print('import 已加')

# 1.2 首页路由：cookie 重定向
old_idx = '''@app.get("/")
def index():
    return _page(os.path.join(STATIC_DIR, "index.html"))'''
new_idx = '''@app.get("/")
def index(request: Request):
    my = request.cookies.get("my_animal")
    if my:
        try:
            conn = database.get_conn()
            row = conn.execute("SELECT id FROM animals WHERE id = ?", (my,)).fetchone()
            conn.close()
            if row:
                return RedirectResponse("/animal/" + my, status_code=302)
        except Exception:
            pass
    return _page(os.path.join(STATIC_DIR, "index.html"))'''
assert old_idx in c
c = c.replace(old_idx, new_idx, 1)
print('首页cookie重定向 已加')

# 1.3 claim POST 成功种 cookie
old_post = '''    conn.commit()
    conn.close()
    return {"ok": True, "animal_id": row["animal_id"], "nickname": nickname}'''
new_post = '''    conn.commit()
    conn.close()
    resp = JSONResponse({"ok": True, "animal_id": row["animal_id"], "nickname": nickname})
    resp.set_cookie("my_animal", row["animal_id"], path="/", max_age=31536000, samesite="lax")
    return resp'''
assert old_post in c
c = c.replace(old_post, new_post, 1)
print('claim POST 种cookie 已加')

open(P, 'w', encoding='utf-8', newline='\n').write(c)
print('main.py 完成')

# ========== 2. 前端种 cookie 兜底 ==========
COOKIE_JS = """      try { document.cookie = 'my_animal=' + animalData.id + '; path=/; max-age=31536000; SameSite=Lax'; } catch(e) {}"""

# 2.1 claim.html：领养成功后
P2 = 'app/static/claim.html'
c2 = open(P2, encoding='utf-8', newline='').read()
c2 = c2.replace('\r\n', '\n')

anchor_a = """              try {
                localStorage.setItem('adopted_' + animalData.id, JSON.stringify({
                  date: new Date().toISOString(),
                  code: code,
                  nickname: nickname
                }));
              } catch(e) {}"""
assert anchor_a in c2, '领养成功锚点'
c2 = c2.replace(anchor_a, anchor_a + """
              try { document.cookie = 'my_animal=' + animalData.id + '; path=/; max-age=31536000; SameSite=Lax'; } catch(e) {}""", 1)
print('claim领养成功种cookie 已加')

# 2.2 绑定按钮
anchor_b = """          try {
            localStorage.setItem('adopted_' + animalData.id, JSON.stringify({
              date: new Date().toISOString(),
              code: code,
              nickname: ''
            }));
          } catch(e) {}"""
assert anchor_b in c2, '绑定按钮锚点'
c2 = c2.replace(anchor_b, anchor_b + """
          try { document.cookie = 'my_animal=' + animalData.id + '; path=/; max-age=31536000; SameSite=Lax'; } catch(e) {}""", 1)
print('绑定按钮种cookie 已加')

# 2.3 已绑定自动跳转
anchor_c = """      try {
        if (localStorage.getItem('adopted_' + animalData.id)) {
          location.replace('/animal/' + animalData.id);
          return;
        }
      } catch(e) {}"""
assert anchor_c in c2, '已绑定跳转锚点'
c2 = c2.replace(anchor_c, """      try {
        if (localStorage.getItem('adopted_' + animalData.id)) {
          try { document.cookie = 'my_animal=' + animalData.id + '; path=/; max-age=31536000; SameSite=Lax'; } catch(e) {}
          location.replace('/animal/' + animalData.id);
          return;
        }
      } catch(e) {}""", 1)
print('已绑定跳转种cookie 已加')

open(P2, 'w', encoding='utf-8', newline='\n').write(c2)
print('claim.html 完成')

# 2.4 index.html 兜底
P3 = 'app/static/index.html'
c3 = open(P3, encoding='utf-8', newline='').read()
c3 = c3.replace('\r\n', '\n')
old_jump = """      if (k && k.indexOf('adopted_') === 0) {
        var id = k.slice(8);
        if (id) { location.replace('/animal/' + id); return; }
      }"""
new_jump = """      if (k && k.indexOf('adopted_') === 0) {
        var id = k.slice(8);
        if (id) {
          try { document.cookie = 'my_animal=' + id + '; path=/; max-age=31536000; SameSite=Lax'; } catch(e) {}
          location.replace('/animal/' + id); return;
        }
      }"""
assert old_jump in c3, 'index跳转锚点'
c3 = c3.replace(old_jump, new_jump, 1)
open(P3, 'w', encoding='utf-8', newline='\n').write(c3)
print('index.html 兜底cookie 已加')
print('全部完成')
