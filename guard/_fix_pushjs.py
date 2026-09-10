# -*- coding: utf-8 -*-
c = open('scripts/_chk_push3.js', encoding='utf-8').read()
c = c.replace("grantPermissions(['notifications']", "grantPermissions(['notifications','push']")
open('scripts/_chk_push3.js', 'w', encoding='utf-8').write(c)
print('OK')
