# -*- coding: utf-8 -*-
"""升级动态信：区域触发式（到新地方→特殊信）+ 随机来信兜底"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
P = 'app/static/animal.html'
c = open(P, encoding='utf-8', newline='').read()
c = c.replace('\r\n', '\n')

# ========== 1. 在 liveLetters 定义前插入 geoRefs + nearestRegion ==========
ANCHOR1 = '      var liveLetters = {'
GEO_JS = r'''      // ===== 🗺️ 区域触发（真实轨迹提炼的真实地标）=====
      var geoRefs = {
        noe: [
          { name: '法国阿尔萨斯', lat: 48.9, lon: 7.1, txt: '它回到了阿尔萨斯的屋顶——烟囱上的大巢还在，邻居家的白鹳也回来了。夏天的阿尔萨斯，麦田金黄，葡萄园飘着新叶的味道。' },
          { name: '西班牙', lat: 40.5, lon: -2.5, txt: '它正在西班牙上空赶路——秋天到了，白鹳们跟着热气流一段一段向南，准备翻过直布罗陀去非洲。' },
          { name: '直布罗陀海峡', lat: 36.1, lon: -5.5, txt: '它盘旋在直布罗陀海峡上空——欧洲和非洲只隔着一道海，它等着一股好风，一鼓作气滑翔过去。' },
          { name: '摩洛哥', lat: 34.3, lon: -6.3, txt: '它落在了摩洛哥的田野里——这里的冬天没有雪，只有暖阳、麦田和吃不完的昆虫。' }
        ],
        turtle: [
          { name: '捷克摩拉维亚', lat: 48.85, lon: 17.0, txt: '它回到了摩拉维亚的麦田——那里有灌浆的小麦、葡萄园的新叶，和它最熟悉的那根电线。' },
          { name: '地中海', lat: 35.5, lon: 20.0, txt: '它正在地中海上空赶路——海面上没有树枝、没有电线，它只能一直扇动翅膀，直到非洲的影子出现在海平线。' },
          { name: '非洲萨赫勒', lat: 13.7, lon: 23.0, txt: '它到了非洲的萨赫勒——金色稀树草原一望无际，金合欢树下是它接下来半年的家。' },
          { name: '爱琴海', lat: 38.2, lon: 24.2, txt: '它飞过了爱琴海——海风从岛屿间穿过来，托着它的翅膀，像有人在后面推着它走。' }
        ],
        herringgull: [
          { name: '荷兰北海海岸', lat: 51.4, lon: 3.6, txt: '它回到了北海海岸——港口、码头和渔市，是银鸥最热闹的食堂。海风一吹，它就知道该往哪飞。' },
          { name: '法国北部', lat: 49.5, lon: 1.5, txt: '它在法国北部的沿海游荡——银鸥沿着海岸找鱼、找风、找一片可以晒太阳的礁石。' },
          { name: '伊比利亚西海岸', lat: 42.5, lon: -8.5, txt: '它正在伊比利亚的西海岸——大西洋的风从这里吹向陆地，浪花里总藏着吃的。' },
          { name: '摩洛哥海岸', lat: 33.4, lon: -7.6, txt: '它到了摩洛哥海岸——冬天这里的海水更暖，鱼群也更密集，银鸥们成群结队来过冬。' }
        ],
        redkite: [
          { name: '德国南部', lat: 48.45, lon: 9.75, txt: '它回到了德国南部的森林——高大树顶上的巢还在，那是它每年夏天都回来的地方。' },
          { name: '法国中部', lat: 45.5, lon: 3.4, txt: '它正在法国中部的天空滑翔——分叉的尾巴像剪刀，轻轻一偏就能转向。' },
          { name: '西班牙西北', lat: 42.53, lon: -5.87, txt: '它到了西班牙西北——那里的冬天比德国温暖，河谷和牧场里总有食物。' }
        ],
        honeybuzzard: [
          { name: '德国南部', lat: 48.6, lon: 9.55, txt: '它回到了德国南部的森林——树冠下的蜂巢里，藏着它的午餐。蜂鹰的羽毛厚得能挡住蜂刺。' },
          { name: '西班牙', lat: 40.5, lon: -1.5, txt: '它正在西班牙上空赶路——蜂鹰要赶在黄蜂停止活动前，飞到温暖的非洲。' },
          { name: '西非几内亚', lat: 7.0, lon: -9.0, txt: '它到了西非的几内亚——热带雨季的森林里，蜜蜂和蜂蛹一年四季都有，是蜂鹰的天堂。' }
        ],
        koa: [
          { name: '加利福尼亚外海', lat: 35.0, lon: -122.5, txt: '它在加州外海的深蓝里巡游——这里是太平洋东岸著名的"白鲨咖啡厅"，海狮和海豹经常出没。' }
        ]
      };
      function nearestRegion(lat, lon) {
        var refs = geoRefs[animalId] || [];
        var best = null, bestD = 1e9;
        for (var gi = 0; gi < refs.length; gi++) {
          var d = Math.pow(refs[gi].lat - lat, 2) + Math.pow(refs[gi].lon - lon, 2);
          if (d < bestD) { bestD = d; best = refs[gi]; }
        }
        if (bestD < 12) return best;  // 约3度内视为该区域
        return null;
      }
'''
assert ANCHOR1 in c, 'liveLetters锚点未找到'
c = c.replace(ANCHOR1, GEO_JS + ANCHOR1, 1)
print('geoRefs已插入')

# ========== 2. 渲染处：区域触发优先 ==========
ANCHOR2 = """      var lv = genLiveLetter(liveS);
          if (lv) liveHtml = '<div class="letter-item live"><div class="letter-head"><span>' + lv.ico + ' ' + lv.t + '</span><span class="letter-st">📬 今日来信</span></div><div class="letter-body">' + lv.body + '</div></div>';"""
NEW_RENDER = """      // 区域触发：它到了新地方 → 特殊信（localStorage 记录上次区域）
      var curReg = null, lastReg = null;
      try {
        curReg = nearestRegion(lpt[1], lpt[0]);
        lastReg = localStorage.getItem('lr_' + animalId);
      } catch (e) {}
      var lv = null;
      if (curReg && curReg !== lastReg) {
        try { localStorage.setItem('lr_' + animalId, curReg.name); } catch (e) {}
        lv = { ico: '📍', t: '来信：它到了一个新地方', body: '<b>' + (a.name || '它') + '</b>到了<b>' + curReg.name + '</b>附近（' + liveS.lat + liveS.latH + ', ' + liveS.lon + liveS.lonH + '）！' + curReg.txt + '（' + liveS.freshTxt + '）它已累计' + (totalKm > 200 ? '飞了' : '移动了') + ' <b>' + liveS.totalKm + ' 公里</b>，与你相伴 ' + liveS.days + ' 天。' };
      } else {
        lv = genLiveLetter(liveS);
      }
          if (lv) liveHtml = '<div class="letter-item live"><div class="letter-head"><span>' + lv.ico + ' ' + lv.t + '</span><span class="letter-st">📬 今日来信</span></div><div class="letter-body">' + lv.body + '</div></div>';"""
assert ANCHOR2 in c, '渲染锚点未找到'
c = c.replace(ANCHOR2, NEW_RENDER, 1)
print('区域触发已插入')

open(P, 'w', encoding='utf-8', newline='\n').write(c)
print('OK')
