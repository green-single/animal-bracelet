# -*- coding: utf-8 -*-
import urllib.request

try:
    r = urllib.request.urlopen('https://animal-bracelet.onrender.com/animal/noe', timeout=60)
    c = r.read().decode('utf-8', 'ignore')
    print('公网状态:', r.status, '| 长度:', len(c))
    print('tabQuiz容器:', 'id="tabQuiz"' in c)
    print('知识Tab项:', 'data-tab="quiz"' in c)
    print('Tab吸顶sticky:', 'position: sticky; top: 0' in c)
    print('分区修复:', "journey: ['todayDyn', 'map-sec', 'stats-sec']" in c)
except Exception as e:
    print('公网异常:', type(e).__name__, e)
