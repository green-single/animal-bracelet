# -*- coding: utf-8 -*-
"""检查公网是否已部署新代码"""
import urllib.request, sys
sys.stdout.reconfigure(encoding='utf-8')
try:
    r = urllib.request.urlopen('https://animal-bracelet.onrender.com/c/HAN-1229', timeout=25)
    html = r.read().decode('utf-8', errors='ignore')
    print('公网status:', r.status)
    checks = {
        'viewport完整': '<meta name="viewport" content="width=device-width' in html,
        'flex-start': 'justify-content: flex-start' in html,
        'story折叠': 'reveal-story.expanded' in html,
        '已绑定跳转': "localStorage.getItem('adopted_'" in html,
        '自动进入': '8 秒后自动进入' in html,
        '断点560': 'max-width: 560px' in html,
    }
    for k, v in checks.items():
        print(k, ':', v)
    print('长度:', len(html))
except Exception as e:
    print('ERR', e)
