# -*- coding: utf-8 -*-
"""瓦片源顺序调整：Esri全球卫星优先（海外无'无卫星图'）"""
P = 'app/static/animal.html'
NL = chr(10)
c = open(P, encoding='utf-8').read()

# 用整块替换：把Esri卫星+地名块移动到第一位
old_first = """    var tileSources = [
      {
        name: '高德卫星+地名',
        layers: [
          { url: 'https://webst01.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}', att: '影像 © 高德地图' },
          { url: 'https://webst01.is.autonavi.com/appmaptile?style=8&x={x}&y={y}&z={z}', att: '地名 © 高德地图', opacity: .9 }
        ]
      },"""
new_first = """    var tileSources = [
      {
        name: '卫星图 · 全球',
        layers: [
          { url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', att: '影像 © Esri' },
          { url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}', att: '地名 © Esri', opacity: .85 }
        ]
      },
      {
        name: '高德卫星+地名',
        layers: [
          { url: 'https://webst01.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}', att: '影像 © 高德地图' },
          { url: 'https://webst01.is.autonavi.com/appmaptile?style=8&x={x}&y={y}&z={z}', att: '地名 © 高德地图', opacity: .9 }
        ]
      },"""

assert old_first in c, 'tileSources头部未找到'
c = c.replace(old_first, new_first)

# 删除原有的Esri卫星块（避免重复）
old_esri = """      {
        name: '卫星+地名',
        layers: [
          { url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', att: '影像 © Esri' },
          { url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}', att: '地名 © Esri', opacity: .85 }
        ]
      },
"""
assert old_esri in c, '原Esri块未找到'
c = c.replace(old_esri, '')

open(P, 'w', encoding='utf-8').write(c)
print('Esri出现次数:', c.count('arcgisonline.com/ArcGIS/rest/services/World_Imagery'))
print('高德卫星出现次数:', c.count('webst01.is.autonavi.com'))
