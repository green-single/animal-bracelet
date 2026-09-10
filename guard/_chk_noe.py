# -*- coding: utf-8 -*-
import sys, sqlite3
sys.stdout.reconfigure(encoding='utf-8')
db = sqlite3.connect('data/animals.db')
db.row_factory = sqlite3.Row
rows = db.execute("SELECT ts, lat, lon FROM track_points WHERE animal_id='noe' ORDER BY ts").fetchall()
print('总点数:', len(rows))
if rows:
    print('起点:', rows[0]['ts'], round(rows[0]['lat'],2), round(rows[0]['lon'],2))
    print('终点:', rows[-1]['ts'], round(rows[-1]['lat'],2), round(rows[-1]['lon'],2))
    # 按月采样找关键位置变化
    import itertools
    last_m = None
    samples = []
    for r in rows:
        m = r['ts'][:7]
        if m != last_m:
            samples.append((m, round(r['lat'],2), round(r['lon'],2)))
            last_m = m
    print('按月首点:')
    for s in samples[:40]:
        print(' ', s[0], 'lat', s[1], 'lon', s[2])
a = db.execute("SELECT * FROM animals WHERE id='noe'").fetchone()
if a:
    print('动物:', dict(a))
