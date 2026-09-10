# -*- coding: utf-8 -*-
import sqlite3, json, sys
sys.stdout.reconfigure(encoding='utf-8')
conn = sqlite3.connect('data/animals.db')
conn.row_factory = sqlite3.Row
rows = conn.execute("SELECT id, name, species, photo_urls FROM animals").fetchall()
for r in rows:
    ph = json.loads(r['photo_urls']) if r['photo_urls'] else []
    first = ph[0] if ph else ''
    print(r['id'], '|', r['name'], '|', r['species'], '|', first)
