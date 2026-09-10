# -*- coding: utf-8 -*-
"""HAN-1229 加进 seed"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
p = 'data/animals_seed.json'
d = json.load(open(p, encoding='utf-8'))
codes = d['codes']
# 去重加 HAN-1229 -> turtle
codes = [c for c in codes if c[0] != 'HAN-1229']
codes.append(['HAN-1229', 'turtle', 'unused', None, None])
d['codes'] = codes
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('HAN-1229 已加入 seed，码总数:', len(codes))
