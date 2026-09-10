# -*- coding: utf-8 -*-
"""main.py 加 manifest/icons 路由"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
P = 'app/main.py'
c = open(P, encoding='utf-8', newline='').read()
c = c.replace('\r\n', '\n')

ANCHOR = '''@app.get("/sw.js")
def sw():
    return FileResponse(os.path.join(STATIC_DIR, "sw.js"), headers=_NO_CACHE_HEADERS)'''

NEW = '''@app.get("/manifest.json")
def manifest():
    return FileResponse(os.path.join(STATIC_DIR, "manifest.json"), headers=_NO_CACHE_HEADERS)


@app.get("/icons/{name}")
def icons(name: str):
    return FileResponse(os.path.join(STATIC_DIR, "icons", name), headers=_NO_CACHE_HEADERS)


@app.get("/sw.js")
def sw():
    return FileResponse(os.path.join(STATIC_DIR, "sw.js"), headers=_NO_CACHE_HEADERS)'''

assert ANCHOR in c, 'main.py 锚点未找到'
c = c.replace(ANCHOR, NEW, 1)
open(P, 'w', encoding='utf-8', newline='\n').write(c)
print('main.py 已加路由')
