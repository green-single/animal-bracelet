# -*- coding: utf-8 -*-
import sqlite3
db = sqlite3.connect('data/animals.db')
n = db.execute("DELETE FROM push_subs WHERE endpoint LIKE '%test%' OR endpoint LIKE '%example%'").rowcount
db.commit()
print('清理测试订阅:', n, '| 剩余:', db.execute('SELECT COUNT(*) FROM push_subs').fetchone()[0])
