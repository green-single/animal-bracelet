# -*- coding: utf-8 -*-
"""补 honeybuzzard 真实地标：西班牙南部（最新真实位置）"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
P = 'app/static/animal.html'
c = open(P, encoding='utf-8', newline='').read()
c = c.replace('\r\n', '\n')
OLD = "          { name: '西班牙', lat: 40.5, lon: -1.5, txt: '它正在西班牙上空赶路——蜂鹰要赶在黄蜂停止活动前，飞到温暖的非洲。' },"
NEW = "          { name: '西班牙南部', lat: 37.0, lon: -4.7, txt: '它正在西班牙南部的安达卢西亚——秋天到了，它沿着海岸线向直布罗陀方向走，准备跨海去非洲过冬。' },\n          { name: '西班牙', lat: 40.5, lon: -1.5, txt: '它正在西班牙上空赶路——蜂鹰要赶在黄蜂停止活动前，飞到温暖的非洲。' },"
assert OLD in c, '锚点未找到'
c = c.replace(OLD, NEW, 1)
open(P, 'w', encoding='utf-8', newline='\n').write(c)
print('已补西班牙南部地标')
