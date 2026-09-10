# -*- coding: utf-8 -*-
"""只改stuck超时 6000→15000"""
P = 'app/static/animal.html'
c = open(P, encoding='utf-8', newline='').read()
crlf = '\r\n' in c
c = c.replace('\r\n', '\n')
n = c.count('}, 6000);')
c = c.replace('}, 6000);', '}, 15000);')
open(P, 'w', encoding='utf-8', newline='\n').write(c)
print('替换数:', n, '| 原CRLF:', crlf, '| 现15000:', c.count('15000'))
