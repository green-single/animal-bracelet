# -*- coding: utf-8 -*-
import re
c = open('app/static/animal.html', encoding='utf-8').read()
for kw in ["facts.parentNode.appendChild", "getElementById('tabQuiz')", 'tabQuiz']:
    idxs = [m.start() for m in re.finditer(re.escape(kw), c)]
    print(kw, ':', idxs)
