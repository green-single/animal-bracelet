# -*- coding: utf-8 -*-
import sqlite3
db = sqlite3.connect('data/animals.db')
db.row_factory = sqlite3.Row
r = db.execute("SELECT code FROM claim_codes WHERE animal_id='turtle' AND status='unused' LIMIT 1").fetchone()
print('turtle测试码:', r['code'] if r else '无')
