# -*- coding: utf-8 -*-
"""根治主屏幕打开不对：
1. manifest display standalone -> browser（iOS/安卓添加主屏幕=当前URL，不再强制打开首页）
2. pwaTip iOS 文案：加"点查看更多"
"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

# 1. manifest
p = 'app/static/manifest.json'
d = json.load(open(p, encoding='utf-8'))
d['display'] = 'browser'
d['name'] = '动物追踪手环'
d['short_name'] = '动物手环'
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('manifest display -> browser')

# 2. pwaTip iOS 文案更新（animal.html / index.html）
NEW_IOS = "how.innerHTML = '点浏览器底部 <b>分享按钮</b> → <b>添加到主屏幕</b><br><span style=\"font-size:11px;color:#8a6d1d;\">如果没看到\"添加到主屏幕\"，点弹窗里的 <b>查看更多</b></span>';"

for page in ['app/static/animal.html', 'app/static/index.html']:
    c = open(page, encoding='utf-8', newline='').read()
    c = c.replace('\r\n', '\n')
    old = "how.innerHTML = '点浏览器底部 <b>分享按钮</b> → <b>添加到主屏幕</b>';"
    if old in c:
        c = c.replace(old, NEW_IOS, 1)
        open(page, 'w', encoding='utf-8', newline='\n').write(c)
        print(page, 'iOS文案已更新')
    else:
        # 可能已经是带 span 的版本
        if "查看更多" in c:
            print(page, '已是新版，跳过')
        else:
            print(page, '警告：未找到iOS锚点')
print('完成')
