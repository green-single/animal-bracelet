# -*- coding: utf-8 -*-
c = open('app/static/animal.html', encoding='utf-8').read()
i = c.find('<main>')
print('=== main开头 ===')
print(c[i:i + 180])
j = c.find('id="tabMine"')
print()
print('=== tabMine后 ===')
print(c[j - 30:j + 220])
