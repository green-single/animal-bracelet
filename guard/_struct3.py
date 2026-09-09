# -*- coding: utf-8 -*-
import re
c = open('app/static/animal.html', encoding='utf-8').read()

k = c.find('tab-item')
seg = c[k:k + 6000]
for kw in ['addEventListener', 'switchTab', 'tab-view']:
    idxs = [m.start() for m in re.finditer(re.escape(kw), seg)]
    if idxs:
        print('tab区', kw, '@', [i + k for i in idxs[:5]])

print()
for kw in ['quizHtml', 'renderQuiz', 'quizList', 'quizWrap', 'quizSection', 'quizData[', 'var quizData']:
    idxs = [m.start() for m in re.finditer(re.escape(kw), c)]
    if idxs:
        print(kw, ':', [i for i in idxs[:6]])
