# -*- coding: utf-8 -*-
"""生成二维码管理清单（Markdown + 每只动物的码）"""
import sqlite3, json, os

conn = sqlite3.connect('data/animals.db')
conn.row_factory = sqlite3.Row
rows = conn.execute('SELECT code, animal_id, status FROM claim_codes ORDER BY animal_id, code').fetchall()
conn.close()

# 动物名映射
names = {
    'noe': 'Noé · 白鹳', 'turtle': 'Lumi · 欧斑鸠', 'redkite': 'Athos · 红鸢',
    'honeybuzzard': 'Mel · 蜂鹰', 'herringgull': 'Silver · 银鸥',
    'koa': 'Koa · 大白鲨(示例)', 'nuna': 'Nuna · 北极燕鸥(示例)',
    'pippin': 'Pippin · 帝企鹅(示例)', 'tembo': 'Tembo · 非洲象(示例)',
    'ava': 'Noel · 绿海龟(2011)', 'kaos': 'Kaos · 座头鲸(1点)',
}
from collections import defaultdict
by_animal = defaultdict(list)
for r in rows:
    by_animal[r['animal_id']].append(f"`{r['code']}`（{r['status']}）")

lines = ['# 🐾 二维码管理清单（公网版）', '',
         f'所有二维码内容均为 `https://animal-bracelet.onrender.com/c/{{码}}`，共 {len(rows)} 个。',
         '', '## 真实数据动物（推荐优先使用）', '']
order = ['noe', 'turtle', 'redkite', 'honeybuzzard', 'herringgull']
for aid in order:
    lines.append(f'### {names.get(aid, aid)}')
    lines.append('')
    lines.append(', '.join(by_animal.get(aid, [])))
    lines.append('')
lines += ['## 示例/旧数据动物（不建议对外发）', '']
for aid in by_animal:
    if aid not in order:
        lines.append(f'### {names.get(aid, aid)}')
        lines.append('')
        lines.append(', '.join(by_animal.get(aid, [])))
        lines.append('')
lines += ['---', '打印稿：`data/print_sheets/二维码打印稿_A4_公网版.pdf`（7页A4）']

out = 'data/qrcodes/二维码管理清单.md'
with open(out, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print('已生成:', out)
