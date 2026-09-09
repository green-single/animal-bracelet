# -*- coding: utf-8 -*-
"""把知识问答从 science 渲染 IIFE 中独立出来，不再依赖 scienceData"""
P = 'app/static/animal.html'
c = open(P, encoding='utf-8').read()

start_marker = '          // 科普知识问答\n          var quizData = {'
end_marker = '            showQuiz();\n          }'

s = c.find(start_marker)
e = c.find(end_marker, s)
assert s > 0 and e > 0, 'quiz段边界未找到 %d %d' % (s, e)
e += len(end_marker)

quiz_block = c[s:e]
print('quiz块长度:', len(quiz_block))

# 原位移除
c = c[:s] + c[e:]

# 在 scienceData 定义前插入独立执行块
anchor = '          var scienceData = {'
idx = c.find(anchor)
assert idx > 0, 'scienceData锚点未找到'
indent = '          '
# 独立执行：包一层 try（原来在 try 内，独立后出错不能影响后续脚本）
block = (
    '          // 科普知识问答（独立模块，不依赖物种科普数据）\n'
    '          try {\n'
    + quiz_block.replace('\n', '\n            ').rstrip() + '\n'
    + '          } catch(e) { console.log(\'科普问答模块错误:\', e); }\n'
    '\n'
)
c = c[:idx] + block + c[idx:]

open(P, 'w', encoding='utf-8').write(c)
print('✅ quiz独立完成')
print('quizData出现:', c.count('var quizData'))
print('tabQuiz目标:', c.count("getElementById('tabQuiz')"))
