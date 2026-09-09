# -*- coding: utf-8 -*-
"""数据赋值后自动渲染（行级处理）"""
P = 'app/static/animal.html'
c = open(P, encoding='utf-8').read()

lines = c.split('\n')
done = False
for i, line in enumerate(lines):
    if 'points = (t.geometry.coordinates || [])' in line:
        insert = [
            '      // 数据就绪：直接显示完整渐变轨迹（清除初始占位线）',
            '      if (points.length > 1) {',
            '        idx = points.length - 1;',
            "        try { updateView(); } catch(e) { console.log('track init err', e); }",
            '      }',
        ]
        lines[i + 1:i + 1] = insert
        done = True
        break

assert done, '数据赋值点未找到'
c = '\n'.join(lines)
open(P, 'w', encoding='utf-8').write(c)
print('✅ 数据加载自动渲染完成')
print('idx定位:', c.count('idx = points.length - 1'))
print('updateView调用:', c.count('try { updateView(); }'))
