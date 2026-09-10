# -*- coding: utf-8 -*-
"""全面检查公网关键功能"""
import urllib.request, sys
sys.stdout.reconfigure(encoding='utf-8')

def get(u):
    try:
        r = urllib.request.urlopen(u, timeout=25)
        return r.read().decode('utf-8', errors='ignore')
    except Exception as e:
        return f'ERR {e}'

# 1. index.html
idx = get('https://animal-bracelet.onrender.com/')
print('=== 首页 ===')
print('  adopted跳转JS:', "location.replace('/animal/' + id)" in idx or 'adopted_' in idx and 'location.replace' in idx)
print('  pwaTip:', 'pwaTip' in idx)

# 2. claim 页
cl = get('https://animal-bracelet.onrender.com/c/HAN-1230')
print('=== 领养页 ===')
print('  已绑定跳转:', "localStorage.getItem('adopted_'" in cl)
print('  绑定到本机按钮:', 'bindMineBtn' in cl)
print('  viewport完整:', '<meta name="viewport" content="width=device-width' in cl)

# 3. 动物页
an = get('https://animal-bracelet.onrender.com/animal/turtle')
print('=== 动物页 ===')
print('  pwaTip:', 'pwaTip' in an)
print('  微信引导:', 'MicroMessenger' in an)

# 4. manifest
try:
    r = urllib.request.urlopen('https://animal-bracelet.onrender.com/manifest.json', timeout=25)
    m = r.read().decode()
    import json
    d = json.loads(m)
    print('=== manifest ===')
    print('  start_url:', d.get('start_url'))
    print('  display:', d.get('display'))
except Exception as e:
    print('manifest ERR', e)
