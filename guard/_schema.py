# -*- coding: utf-8 -*-
import sqlite3, sys
sys.stdout.reconfigure(encoding='utf-8')
conn = sqlite3.connect('data/animals.db')
rows = conn.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='animals'").fetchall()
for r in rows:
    print(r[0])
