# -*- coding: utf-8 -*-
"""临时加错误日志定位"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
P = 'app/static/animal.html'
c = open(P, encoding='utf-8', newline='').read()
c = c.replace('\r\n', '\n')
OLD = "          if (lv2) liveHtml = '<div class=\"letter-item live\"><div class=\"letter-head\"><span>' + lv2.ico + ' ' + lv2.t + '</span><span class=\"letter-st\">📬 今日来信</span></div><div class=\"letter-body\">' + lv2.body + '</div></div>';\n        } catch (e) {}"
NEW = "          if (lv2) liveHtml = '<div class=\"letter-item live\"><div class=\"letter-head\"><span>' + lv2.ico + ' ' + lv2.t + '</span><span class=\"letter-st\">📬 今日来信</span></div><div class=\"letter-body\">' + lv2.body + '</div></div>';\n        } catch (e) { console.log('liveLetter err:', e); }"
if OLD in c:
    c = c.replace(OLD, NEW, 1)
    print('已加日志')
else:
    print('锚点未找到')
open(P, 'w', encoding='utf-8', newline='\n').write(c)
