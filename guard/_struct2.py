# -*- coding: utf-8 -*-
import re
c = open('app/static/animal.html', encoding='utf-8').read()

# tab内容容器
for m in re.finditer(r'id="(tab[A-Z][^"]*)"', c):
    pos = m.start()
    print(m.group(1), '@', pos, ':', c[pos - 80:pos + 120].replace('\n', ' ')[:200])
    print()

# quiz渲染逻辑
for kw in ['quizSection', 'quiz-section', 'renderQuiz', 'quizData', 'quiz-container', 'quizList', 'quizBox']:
    for m in re.finditer(re.escape(kw), c):
        pos = m.start()
        print(kw, '@', pos, ':', c[max(0, pos - 70):pos + 100].replace('\n', ' ')[:170])
        print()
        break
