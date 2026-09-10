# -*- coding: utf-8 -*-
import sqlite3
db = sqlite3.connect('data/animals.db')
db.execute("UPDATE claim_codes SET status='unused', claimed_at=NULL, nickname=NULL WHERE code='KHYM-NVWZ'")
db.commit()
r = db.execute("SELECT code, status FROM claim_codes WHERE code='KHYM-NVWZ'").fetchone()
print('重置后:', r)
