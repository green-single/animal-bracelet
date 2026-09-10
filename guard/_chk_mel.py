# -*- coding: utf-8 -*-
import sys, sqlite3
sys.stdout.reconfigure(encoding='utf-8')
db = sqlite3.connect('data/animals.db')
db.row_factory = sqlite3.Row
rows = db.execute("SELECT ts, lat, lon FROM track_points WHERE animal_id='honeybuzzard' ORDER BY ts").fetchall()
last_m = None
for r in rows:
    m = r['ts'][:7]
    if m != last_m:
        print(m, round(r['lat'],2), round(r['lon'],2))
        last_m = m
