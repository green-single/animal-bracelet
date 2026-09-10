# -*- coding: utf-8 -*-
"""生成全部领养码清单"""
import sqlite3, sys
sys.stdout.reconfigure(encoding='utf-8')
conn = sqlite3.connect('data/animals.db')
conn.row_factory = sqlite3.Row

# 动物名称映射
names = {
    'noe': 'Noé 白鹳',
    'turtle': 'Lumi 欧斑鸠',
    'herringgull': 'Silver 银鸥',
    'redkite': 'Athos 红鸢',
    'honeybuzzard': 'Mel 蜂鹰',
    'koa': 'Koa 大白鲨(示例)',
    'ava': 'Noel 绿海龟',
    'tembo': 'Tembo 非洲象',
    'pippin': 'Pippin 帝企鹅',
    'nuna': 'Nuna 北极燕鸥',
    'nuri': 'Nuri 绿海龟',
    'kaos': 'Kaos 座头鲸',
}
# 检查表结构
cols = [r['name'] for r in conn.execute("PRAGMA table_info(claim_codes)")]
print('claim_codes列:', cols)
rows = conn.execute("SELECT * FROM claim_codes ORDER BY animal_id, code").fetchall()
lines = []
cur_animal = None
count = {}
for r in rows:
    aid = r['animal_id']
    code = r['code']
    # 状态
    claimed = ''
    for k in ('claimed', 'used', 'status', 'claimed_by', 'claimed_at'):
        if k in r.keys() and r[k]:
            claimed = str(r[k])
    if aid != cur_animal:
        if cur_animal is not None:
            lines.append('')
        lines.append('## ' + names.get(aid, aid))
        lines.append('| 码 | 状态 |')
        lines.append('|---|---|')
        cur_animal = aid
    count[aid] = count.get(aid, 0) + 1
    st = '已领养' if claimed else '可用'
    lines.append('| %s | %s |' % (code, st))

total = sum(count.values())
print('共', total, '个码')
out = '\n'.join(lines)
fn = 'qrcodes/全部领养码清单.md'
open(fn, 'w', encoding='utf-8', newline='\n').write('# 动物追踪手环 · 全部领养码清单\n\n' + out + '\n')
print('已写入', fn)
