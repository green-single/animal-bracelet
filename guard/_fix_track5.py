# -*- coding: utf-8 -*-
"""补：起点绑定后插 push(startDot)"""
P = 'app/static/animal.html'
NL = chr(10)
c = open(P, encoding='utf-8').read()
if 'trackLayers.push(startDot)' in c:
    print('已存在')
else:
    lines = c.split(NL)
    done = False
    for i, line in enumerate(lines):
        if ".addTo(map).bindTooltip('起点');" in line and 'startDot' in lines[i - 1] if i > 0 else False:
            lines.insert(i + 1, '    trackLayers.push(startDot);')
            done = True
            break
    assert done, '起点绑定行未找到'
    c = NL.join(lines)
    open(P, 'w', encoding='utf-8').write(c)
    print('OK startDot入列完成')
    print('startDot入列:', c.count('trackLayers.push(startDot)'))
