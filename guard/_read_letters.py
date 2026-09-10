# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
c = open('app/static/animal.html', encoding='utf-8').read()
m = re.search(r"customLetters\s*=\s*\{.*?turtle:\s*\[\s*(.*?)\n\s*\],", c, re.S)
if m:
    seg = m.group(1)
    titles = re.findall(r"title:\s*['\"]([^'\"]+)['\"]", seg)
    days = re.findall(r"day:\s*(\d+)", seg)
    print('信件数:', len(titles))
    for d, t in zip(days, titles):
        print(f'第{d}天 | {t}')
else:
    print('未匹配到turtle段，搜索customLetters...')
    i = c.find('customLetters')
    print(c[i:i+300])
