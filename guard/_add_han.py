# -*- coding: utf-8 -*-
"""插入 HAN-1229 自定义码 -> turtle"""
import sqlite3, sys
sys.stdout.reconfigure(encoding='utf-8')
conn = sqlite3.connect('data/animals.db')
print('表结构:', conn.execute('PRAGMA table_info(claim_codes)').fetchall())
try:
    conn.execute("INSERT INTO claim_codes (code, animal_id, status) VALUES ('HAN-1229', 'turtle', 'unused')")
    conn.commit()
    print('HAN-1229 已插入 -> turtle')
except Exception as e:
    print('插入失败:', e)
for r in conn.execute("SELECT code, animal_id, status FROM claim_codes WHERE code LIKE '%HAN%'"):
    print(r)
