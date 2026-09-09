# -*- coding: utf-8 -*-
c = open('app/static/animal.html', encoding='utf-8').read()
print(c[156376:156700])
print('......')
i = c.find("var letterList = document.getElementById('letterList')")
print(c[i-700:i+200])
