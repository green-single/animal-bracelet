# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
import sqlite3
from collections import Counter

db = sqlite3.connect('data/animals.db')
db.row_factory = sqlite3.Row
a = db.execute("SELECT * FROM animals WHERE id='turtle'").fetchone()
print('物种:', a['name'], '| 学名:', a['species'])
print('故事(前300字):', (a['story'] or '')[:300])
print('来源:', a['origin'])
print('照片数:', len((a['photo_urls'] or '').split(',')))
print()

pts = db.execute("SELECT lat, lon, ts FROM track_points WHERE animal_id='turtle' ORDER BY ts").fetchall()
print('总点数:', len(pts))
print('时间范围:', pts[0]['ts'], '→', pts[-1]['ts'])
months = Counter(p['ts'][:7] for p in pts)
print('按月:', dict(sorted(months.items())))
print('每年点数:', dict(sorted(Counter(p['ts'][:4] for p in pts).items())))

# 每月首个+最后点
print('\n每月轨迹概况:')
prev = None
for p in pts:
    m = p['ts'][:7]
    if m != prev:
        print(f'  {m} 首点: {p["lat"]:.1f}°,{p["lon"]:.1f}°', end='')
        prev = m
    elif p['ts'][:7] != pts[pts.index(p)-1]['ts'][:7]:
        pass
print()
# 每季末点
print('\n每月末点:')
groups = {}
for p in pts:
    groups[p['ts'][:7]] = p
for m in sorted(groups):
    p = groups[m]
    print(f'  {m} 末点: {p["lat"]:.1f}°,{p["lon"]:.1f}°')
print('\n最后8点:')
for p in pts[-8:]:
    print(f'  {p["ts"]} {p["lat"]:.2f}°,{p["lon"]:.2f}°')

# 总距离（haversine）
import math
def hav(a, b):
    R = 6371
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dp = math.radians(b[0]-a[0]); dl = math.radians(b[1]-a[1])
    x = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2*R*math.asin(math.sqrt(x))
total = 0
for i in range(1, len(pts)):
    total += hav((pts[i-1]['lat'], pts[i-1]['lon']), (pts[i]['lat'], pts[i]['lon']))
print(f'\n总迁徙距离约: {total:.0f} km')

# 经纬度范围
lats = [p['lat'] for p in pts]; lons = [p['lon'] for p in pts]
print(f'纬度: {min(lats):.1f}~{max(lats):.1f} | 经度: {min(lons):.1f}~{max(lons):.1f}')
