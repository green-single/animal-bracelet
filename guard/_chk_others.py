# -*- coding: utf-8 -*-
import sys, sqlite3
sys.stdout.reconfigure(encoding='utf-8')
db = sqlite3.connect('data/animals.db')
db.row_factory = sqlite3.Row
for aid in ['herringgull', 'redkite', 'honeybuzzard', 'koa']:
    rows = db.execute("SELECT ts, lat, lon FROM track_points WHERE animal_id=? ORDER BY ts", (aid,)).fetchall()
    print('=====', aid, '总点数:', len(rows))
    if not rows:
        continue
    print('起点:', rows[0]['ts'][:10], round(rows[0]['lat'],2), round(rows[0]['lon'],2))
    print('终点:', rows[-1]['ts'][:10], round(rows[-1]['lat'],2), round(rows[-1]['lon'],2))
    last_m = None
    for r in rows:
        m = r['ts'][:7]
        if m != last_m:
            print(' ', m, round(r['lat'],2), round(r['lon'],2))
            last_m = m
