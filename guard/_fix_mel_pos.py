# -*- coding: utf-8 -*-
"""修正 Mel：初遇信真实位置+补摩洛哥南部地标"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
P = 'app/static/animal.html'
c = open(P, encoding='utf-8', newline='').read()
c = c.replace('\r\n', '\n')

# 1. 初遇信真实位置
OLD1 = "此刻它正在<b>西班牙南部</b>（37.0°N, 4.7°W）上空——秋天到了，它正赶着去非洲，那里有它最爱的蜂巢。"
NEW1 = "此刻它正在<b>摩洛哥南部</b>（29.9°N, 6.8°W）——撒哈拉的边缘，秋天到了，它正跨过沙漠赶去西非，那里有它最爱的蜂巢。"
assert OLD1 in c, '初遇信锚点未找到'
c = c.replace(OLD1, NEW1, 1)

# 2. geoRefs 补摩洛哥南部
OLD2 = "          { name: '西班牙南部', lat: 37.0, lon: -4.7, txt: '它正在西班牙南部的安达卢西亚——秋天到了，它沿着海岸线向直布罗陀方向走，准备跨海去非洲过冬。' },"
NEW2 = "          { name: '摩洛哥南部', lat: 29.9, lon: -6.75, txt: '它正在摩洛哥南部的撒哈拉边缘——秋天到了，蜂鹰们正跨过这片沙漠，赶往西非的雨季森林。' },"
assert OLD2 in c, 'geoRefs锚点未找到'
c = c.replace(OLD2, NEW2, 1)

open(P, 'w', encoding='utf-8', newline='\n').write(c)
print('已修正Mel位置')
