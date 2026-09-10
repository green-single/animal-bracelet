# -*- coding: utf-8 -*-
import sys, sqlite3, json
sys.stdout.reconfigure(encoding='utf-8')
conn = sqlite3.connect('data/animals.db')
conn.row_factory = sqlite3.Row
rows = conn.execute("SELECT id, name, species, photos FROM animals").fetchall()
for r in rows:
    ph = json.loads(r['photos']) if r['photos'] else []
    first = ''
    if ph:
        first = ph[0].get('url') if isinstance(ph[0], dict) else str(ph[0])
    print(r['id'], '|', r['name'], '|', r['species'], '|', first)
