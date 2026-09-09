# -*- coding: utf-8 -*-
"""列出当前每只动物的码，确定需要补多少公网码"""
import sqlite3, json

conn = sqlite3.connect('data/animals.db')
conn.row_factory = sqlite3.Row

print('=== 数据库里的领养码 ===')
rows = conn.execute('SELECT code, animal_id, status FROM claim_codes ORDER BY animal_id').fetchall()
from collections import defaultdict
by_animal = defaultdict(list)
for r in rows:
    by_animal[r['animal_id']].append(r['code'])
for aid, codes in by_animal.items():
    print(f'{aid}: {len(codes)}个 {codes[:4]}...')

print('\n=== codes.json里的公网码 ===')
with open('data/qrcodes/codes.json', encoding='utf-8') as f:
    meta = json.load(f)
pub = [m for m in meta if 'onrender.com' in m['url']]
for m in pub:
    print(f"  {m['code']} -> {m['animal_id']} ({m['type']}) {m['url']}")

conn.close()
