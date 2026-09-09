# -*- coding: utf-8 -*-
"""占位线入列：行级处理（锚点=points[0]）"""
P = 'app/static/animal.html'
NL = chr(10)
c = open(P, encoding='utf-8').read()
lines = c.split(NL)

done1 = done2 = done3 = False
for i, line in enumerate(lines):
    if not done1 and 'lineLayer = L.polyline' in line:
        for j in range(i, min(i + 5, len(lines))):
            if '}).addTo(map);' in lines[j]:
                lines.insert(j + 1, '    trackLayers.push(lineLayer);')
                done1 = True
                break
    if not done2 and 'L.circleMarker(points' in line:
        # 把 circleMarker 赋给 startDot（仅 initMap 起点处，且尚未赋值）
        if 'var startDot' not in line:
            lines[i] = lines[i].replace('L.circleMarker(points',
                                        'var startDot = L.circleMarker(points', 1)
            done2 = True
    if not done3 and 'var startDot' in lines[i] and '.addTo(map).bindTooltip' in lines[i]:
        # 起点绑定行后面插入入列
        lines.insert(i + 1, '    trackLayers.push(startDot);')
        done3 = True
    if done1 and done2 and done3:
        break

assert done1 and done2, '修改失败 %s %s %s' % (done1, done2, done3)
c = NL.join(lines)
open(P, 'w', encoding='utf-8').write(c)
print('OK 占位线入列')
print('lineLayer入列:', c.count('trackLayers.push(lineLayer)'))
print('startDot:', c.count('var startDot'))
print('startDot入列:', c.count('trackLayers.push(startDot)'))
