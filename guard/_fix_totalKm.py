# -*- coding: utf-8 -*-
"""修复totalKm公式：pts变量+方括号（行级）"""
P = 'app/static/animal.html'
NL = chr(10)
c = open(P, encoding='utf-8').read()
lines = c.split(NL)

# 找到 totalKm 块并整体替换
start = None
for i, l in enumerate(lines):
    if '真实累计飞行距离' in l:
        start = i
        break
assert start is not None, 'totalKm块未找到'

new_block = [
    "      // 真实累计飞行距离（haversine）",
    "      var totalKm = 0;",
    "      if (pts && pts.length > 1) {",
    "        var R_ = 6371;",
    "        for (var pi_ = 1; pi_ < pts.length; pi_++) {",
    "          var p1_ = pts[pi_ - 1], p2_ = pts[pi_];",
    "          var dLat_ = (p2_[1] - p1_[1]) * Math.PI / 180;",
    "          var dLon_ = (p2_[0] - p1_[0]) * Math.PI / 180;",
    "          var a_ = Math.sin(dLat_ / 2) * Math.sin(dLat_ / 2) +",
    "                   Math.cos(p1_[1] * Math.PI / 180) * Math.cos(p2_[1] * Math.PI / 180) *",
    "                   Math.sin(dLon_ / 2) * Math.sin(dLon_ / 2);",
    "          totalKm += R_ * 2 * Math.atan2(Math.sqrt(a_), Math.sqrt(1 - a_));",
    "        }",
    "      }",
]
# 找到块结束（下一个 'var letters =' 前）
end = None
for i in range(start, start + 20):
    if 'var letters =' in lines[i]:
        end = i
        break
assert end is not None, 'letters锚点未找到'
lines[start:end] = new_block

c = NL.join(lines)
open(P, 'w', encoding='utf-8').write(c)
# 验证
ok1 = 'pts[pi_]' in c
ok2 = 'p2_[1]' in c and 'p1_[1]' in c
ok3 = 'p2_[0]' in c
print('修复完成 | pts:', ok1, '| dLat方括号:', ok2, '| dLon方括号:', ok3)
