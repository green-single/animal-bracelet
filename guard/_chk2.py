# -*- coding: utf-8 -*-
c = open('_serve_chk.html', encoding='utf-8').read()
print('返回HTML长度:', len(c))
print('tabQuiz总出现:', c.count('tabQuiz'))
print('facts.parentNode.appendChild:', c.count('facts.parentNode.appendChild'))
print("getElementById('tabQuiz'):", c.count("getElementById('tabQuiz')"))
print('id="tabQuiz":', c.count('id="tabQuiz"'))
