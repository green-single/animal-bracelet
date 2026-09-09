# -*- coding: utf-8 -*-
c = open('app/static/animal.html', encoding='utf-8').read()
i = c.find('id="tabBar"')
j = c.find('<main>')
print('tabBar HTML@', i, '| main@', j, '| tabBar在main后:', i > j)
print('上下文:', c[i - 60:i + 110].replace('\n', ' '))
