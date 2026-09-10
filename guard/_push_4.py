# -*- coding: utf-8 -*-
"""加 /sw.js 路由"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
P = 'app/main.py'
c = open(P, encoding='utf-8', newline='').read()
c = c.replace('\r\n', '\n')

anchor = '@app.get("/photos/{filename}")'
add = '''@app.get("/sw.js")
def sw_file():
    """Service Worker（根路径，scope=/ 全站推送）"""
    return FileResponse(os.path.join(STATIC_DIR, "sw.js"), headers=_NO_CACHE_HEADERS)


@app.get("/photos/{filename}")'''
assert anchor in c, 'photos锚点未找到'
c = c.replace(anchor, add, 1)
open(P, 'w', encoding='utf-8', newline='\n').write(c)
print('sw.js路由已加 | count:', c.count('/sw.js'))
