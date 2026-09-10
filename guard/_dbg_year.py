# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
c = open('app/static/animal.html', encoding='utf-8').read()
# 找年份筛选逻辑
for kw in ['yearFilter', 'yearSelect', '年份', 'filterYear', 'rangeFilter', 'timeRange']:
    idxs = [m.start() for m in re.finditer(re.escape(kw), c)]
    print(kw, ':', idxs[:10])
