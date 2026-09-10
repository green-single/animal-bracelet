# -*- coding: utf-8 -*-
"""修复：今日来信移到正确的信渲染段 + 修正 lat/lon 索引"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
P = 'app/static/animal.html'
c = open(P, encoding='utf-8', newline='').read()
c = c.replace('\r\n', '\n')

# ========== 1. 删除 diary 函数里的今日来信块 ==========
START = "            // 📬 今日来信（领养后显示，随机模板+真实数据）"
END = """          if (lv) liveHtml = '<div class="letter-item live"><div class="letter-head"><span>' + lv.ico + ' ' + lv.t + '</span><span class="letter-st">📬 今日来信</span></div><div class="letter-body">' + lv.body + '</div></div>';
        } catch (e) {}
      }
      var html = '';"""
if START in c:
    i0 = c.index(START)
    i1 = c.index(END) + len(END)
    c = c[:i0] + c[i1:]
    print('已删除diary中的错误块')
else:
    print('WARN: diary中的块不存在，跳过删除')

# ========== 2. 在真正的信渲染段插入正确版 ==========
ANCHOR = "      var html = '';\n      letters.forEach(function (L) {"
LIVE_OK = """      // 📬 今日来信（领养后显示：到新地方→特殊信；平时→偶尔随机来信，40%概率+每天最多一封）
      var liveHtml = '';
      if (days >= 0 && pts && pts.length) {
        try {
          var lpt = pts[pts.length - 1];
          var lts = timestamps[timestamps.length - 1];
          var _da2 = 0;
          try { _da2 = Math.max(0, Math.floor((Date.now() - new Date(lts.replace(' ', 'T')).getTime()) / 86400000)); } catch (e) {}
          var _fresh2 = _da2 === 0 ? '今天，它刚刚更新了定位' : _da2 === 1 ? '昨天，它还在路上' : _da2 <= 7 ? _da2 + ' 天前，它留下了新的足迹' : '它正在一段安静的旅途中';
          var liveS2 = {
            lat: _sfmt(Math.abs(lpt[0])), latH: lpt[0] >= 0 ? '°N' : '°S',
            lon: _sfmt(Math.abs(lpt[1])), lonH: lpt[1] >= 0 ? '°E' : '°W',
            totalKm: Math.round(totalKm),
            days: days,
            freshTxt: _fresh2,
            fmtD: fmtD(lts)
          };
          var curReg2 = null, lastReg2 = null;
          try {
            curReg2 = nearestRegion(lpt[0], lpt[1]);
            lastReg2 = localStorage.getItem('lr_' + animalId);
          } catch (e) {}
          var lv2 = null;
          if (curReg2 && curReg2 !== lastReg2) {
            try { localStorage.setItem('lr_' + animalId, curReg2.name); } catch (e) {}
            lv2 = { ico: '📍', t: '来信：它到了一个新地方', body: '<b>' + (a.name || '它') + '</b>到了<b>' + curReg2.name + '</b>附近（' + liveS2.lat + liveS2.latH + ', ' + liveS2.lon + liveS2.lonH + '）！' + curReg2.txt + '（' + liveS2.freshTxt + '）它已累计' + (totalKm > 200 ? '飞了' : '移动了') + ' <b>' + liveS2.totalKm + ' 公里</b>，与你相伴 ' + liveS2.days + ' 天。' };
          } else {
            var _todayS = new Date().toDateString();
            var _lastRand = null;
            try { _lastRand = localStorage.getItem('lr_rand_' + animalId); } catch (e) {}
            if (_lastRand !== _todayS && Math.random() < 0.4) {
              try { localStorage.setItem('lr_rand_' + animalId, _todayS); } catch (e) {}
              lv2 = genLiveLetter(liveS2);
            }
          }
          if (lv2) liveHtml = '<div class="letter-item live"><div class="letter-head"><span>' + lv2.ico + ' ' + lv2.t + '</span><span class="letter-st">📬 今日来信</span></div><div class="letter-body">' + lv2.body + '</div></div>';
        } catch (e) {}
      }
      var html = liveHtml;
      letters.forEach(function (L) {"""
if ANCHOR in c:
    c = c.replace(ANCHOR, LIVE_OK, 1)
    print('已在信渲染段插入')
else:
    print('ERROR: 信渲染段锚点未找到')

open(P, 'w', encoding='utf-8', newline='\n').write(c)
print('OK')
