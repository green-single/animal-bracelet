# -*- coding: utf-8 -*-
"""各页面 head 加 PWA 链接"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

PWA_HEAD = '''  <link rel="manifest" href="/manifest.json">
  <link rel="apple-touch-icon" href="/icons/apple-touch-icon.png">
  <meta name="theme-color" content="#12796F">
  <meta name="mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">'''

for page in ['app/static/index.html', 'app/static/animal.html', 'app/static/claim.html', 'app/static/admin.html']:
    c = open(page, encoding='utf-8', newline='').read()
    c = c.replace('\r\n', '\n')
    anchor = '<meta name="viewport"'
    assert anchor in c, page + ' viewport 锚点未找到'
    # 在 viewport 后插入
    c = c.replace(anchor, anchor + '\n' + PWA_HEAD, 1)
    open(page, 'w', encoding='utf-8', newline='\n').write(c)
    print(page, '已加PWA链接')
