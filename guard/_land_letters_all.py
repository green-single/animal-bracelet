# -*- coding: utf-8 -*-
"""动态来信系统 + Noé专属信 + 其他动物基础信"""
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
P = 'app/static/animal.html'
c = open(P, encoding='utf-8', newline='').read()
c = c.replace('\r\n', '\n')

# ============ 1. 插入 liveLetters 定义（在 var customLetters = { 前） ============
ANCHOR1 = '      var customLetters = {'
LIVE_JS = r'''      // ===== 📬 动态来信（真实数据 + 随机模板，每次打开都可能不同）=====
      var _rnd = function (arr) { return arr[Math.floor(Math.random() * arr.length)]; };
      var _mon = new Date().getMonth() + 1;
      var _sea = (_mon >= 3 && _mon <= 5) ? 0 : (_mon >= 6 && _mon <= 8) ? 1 : (_mon >= 9 && _mon <= 11) ? 2 : 3;
      var _seaTxt = ['春天', '夏天', '秋天', '冬天'][_sea];
      function _sfmt(n) { return Math.abs(n).toFixed(1); }
      var liveLetters = {
        noe: [
          { ico: '🪶', t: '来信：它在天上', body: function (s) { return 'Noé 的最新足迹在 <b>' + s.lat + s.latH + ', ' + s.lon + s.lonH + '</b>（' + s.freshTxt + '）。' + (_sea === 0 ? '春天正把白鹳们从非洲唤回欧洲，它们沿着古老的路线向北，靠着一路的热气流滑翔，几乎不用扇翅膀。' : _sea === 1 ? '夏天是白鹳在法国阿尔萨斯屋顶上养家的季节——大巢里伸出几颗毛茸茸的小脑袋，等着爸爸妈妈带鱼回来。' : _sea === 2 ? '秋风一起，欧洲的白鹳就开始集结了——它们要在直布罗陀上空汇合，然后跟着热气流翻过撒哈拉。Noé 已经在路上。' : '此刻的 Noé 应该在西非的湿地或田野里过冬，那里有吃不完的蛙和昆虫，太阳也比欧洲慷慨得多。') + '它已累计飞了 <b>' + s.totalKm + ' 公里</b>，与你相伴 ' + s.days + ' 天。'; } },
          { ico: '💌', t: '来信：屋顶上的家', body: function (s) { return '白鹳不鸣叫，它们用喙说话——上下喙快速敲击，发出哒哒哒的声响，邻居一听就知道：这家人回来了。Noé 每年夏天都会回到阿尔萨斯的屋顶，修补同一个巢。它最新一次现身：' + s.fmtD + '，在 <b>' + s.lat + s.latH + ', ' + s.lon + s.lonH + '</b>。'; } },
          { ico: '🧭', t: '来信：五年的路', body: function (s) { return '从 2021 年夏天戴上追踪器算起，Noé 已经在欧洲与非洲之间往返了 <b>' + s.totalKm + ' 公里</b>——足够绕地球半圈还多。白鹳认得路，靠地磁、太阳，也靠记忆里那片熟悉的田野。它最近一次定位：' + s.fmtD + '，' + s.freshTxt + '。'; } },
          { ico: '🌍', t: '来信：此刻的它', body: function (s) { return '此刻的 Noé 在 <b>' + s.lat + s.latH + ', ' + s.lon + s.lonH + '</b> 附近' + (_sea === 2 ? '——秋天了，它正跟着热气流一段一段向南，今晚也许会停在一根高压线塔上过夜。' : _sea === 0 ? '——春天了，它正一路向北，赶回阿尔萨斯的屋顶。' : _sea === 1 ? '——夏天了，它正站在巢边看护幼鸟，红嘴红腿在阳光下特别显眼。' : '——冬天了，它正在西非的田野里散步，长喙一探一探地找吃的。') + '它已经为你飞了 <b>' + s.totalKm + ' 公里</b>。'; } },
          { ico: '🕊️', t: '来信：守护者的目光', body: function (s) { return '今天是你守护 Noé 的第 <b>' + s.days + '</b> 天。它不知道你的名字，但它飞过的每一段路，都有一道目光在云端跟着。' + s.freshTxt + '它最新足迹：<b>' + s.lat + s.latH + ', ' + s.lon + s.lonH + '</b>。'; } }
        ],
        herringgull: [
          { ico: '🌊', t: '来信：海风里的它', body: function (s) { return 'Silver 最新足迹在 <b>' + s.lat + s.latH + ', ' + s.lon + s.lonH + '</b>（' + s.freshTxt + '）。银鸥最懂海风——它顺着风滑翔，贴着浪尖飞，饿了就俯冲下去叼一条鱼。它已累计移动 <b>' + s.totalKm + ' 公里</b>，与你相伴 ' + s.days + ' 天。'; } },
          { ico: '🦐', t: '来信：什么都吃', body: function (s) { return '银鸥是海边的杂食家：小鱼、螃蟹、海胆，甚至是面包和薯条，它都来者不拒。它最新一次定位：' + s.fmtD + '，在 <b>' + s.lat + s.latH + ', ' + s.lon + s.lonH + '</b> 附近。港口、码头、渔市——跟着银鸥，就能找到最热闹的海岸。'; } },
          { ico: '📣', t: '来信：海港的声音', body: function (s) { return '你听过银鸥的叫声吗？一声拖长的 kyow——那是海港的背景音乐。Silver 最近现身于 <b>' + s.lat + s.latH + ', ' + s.lon + s.lonH + '</b>，' + s.freshTxt + '。它已经陪你走过 <b>' + s.totalKm + ' 公里</b> 的海岸线。'; } },
          { ico: '💌', t: '来信：守护者的第' + 'N' + '天', body: function (s) { return '相伴第 <b>' + s.days + '</b> 天。海鸥的一生很长，能活三十多年——它们记得每一片港口，也记得谁对它好。Silver 现在在 <b>' + s.lat + s.latH + ', ' + s.lon + s.lonH + '</b>，' + s.freshTxt + '。'; } }
        ],
        redkite: [
          { ico: '🪁', t: '来信：天空的滑翔家', body: function (s) { return 'Athos 最新足迹在 <b>' + s.lat + s.latH + ', ' + s.lon + s.lonH + '</b>（' + s.freshTxt + '）。红鸢是滑翔大师——翅膀几乎不动，只靠气流就能在天上盘旋半天。它分叉的尾巴像一把剪刀，调头时轻轻一偏，姿态优雅得像一场飞行表演。累计 <b>' + s.totalKm + ' 公里</b>。'; } },
          { ico: '🍖', t: '来信：不挑食的猛禽', body: function (s) { return '红鸢不挑食：腐肉、蚯蚓、小鼠、甚至人类留下的食物残渣，它都乐于清理。它最新一次定位：' + s.fmtD + '，在 <b>' + s.lat + s.latH + ', ' + s.lon + s.lonH + '</b> 上空盘旋。大自然最尽责的清道夫，就是它。'; } },
          { ico: '🌬️', t: '来信：气流之上', body: function (s) { return (_sea === 0 ? '春天，红鸢开始筑巢——它们喜欢高大的树，巢搭在高高的树杈上。' : _sea === 1 ? '夏天，小红鸢在巢里练习扇翅膀，父母轮流带食物回来。' : _sea === 2 ? '秋天，北方来的红鸢会向南游荡，寻找食物更充足的地方。' : '冬天，红鸢聚在河谷和牧场边，靠腐肉和小动物过冬。') + 'Athos 现在在 <b>' + s.lat + s.latH + ', ' + s.lon + s.lonH + '</b>，' + s.freshTxt + '。'; } },
          { ico: '💌', t: '来信：守护者的第' + 'N' + '天', body: function (s) { return '你守护 Athos 已经 <b>' + s.days + '</b> 天。它的翅膀掠过 <b>' + s.totalKm + ' 公里</b>——风知道，你也知道。最新足迹：<b>' + s.lat + s.latH + ', ' + s.lon + s.lonH + '</b>。'; } }
        ],
        honeybuzzard: [
          { ico: '🐝', t: '来信：蜂巢美食家', body: function (s) { return 'Mel 最新足迹在 <b>' + s.lat + s.latH + ', ' + s.lon + s.lonH + '</b>（' + s.freshTxt + '）。蜂鹰有个独门绝技——吃黄蜂：厚实的羽毛挡住蜂刺，利爪刨开蜂巢，专挑蜂蛹吃。它是猛禽里最特别的美食家。累计 <b>' + s.totalKm + ' 公里</b>。'; } },
          { ico: '✈️', t: '来信：撒哈拉的跨越者', body: function (s) { return '蜂鹰是真正的长距离迁徙专家——每年从欧洲飞到非洲，跨过撒哈拉沙漠。它们会在海峡上空盘旋，等风，也等热气流。Mel 已累计飞了 <b>' + s.totalKm + ' 公里</b>，最近一次定位：' + s.fmtD + '。'; } },
          { ico: '🍂', t: '来信：秋天出发', body: function (s) { return (_sea === 2 ? '夏末秋初，欧洲的蜂鹰会成群结队出发——它们要赶在黄蜂停止活动之前，飞到温暖的非洲。' : _sea === 0 ? '春天，蜂鹰从非洲返回欧洲，一路跟着花开的节奏。' : '此刻的 Mel 在 <b>' + s.lat + s.latH + ', ' + s.lon + s.lonH + '</b>，' + s.freshTxt + '。') + '它的小爪子里，藏着一个关于蜂巢的秘密。'; } },
          { ico: '💌', t: '来信：守护者的第' + 'N' + '天', body: function (s) { return '相伴第 <b>' + s.days + '</b> 天。Mel 飞过的 <b>' + s.totalKm + ' 公里</b> 里，有蜂巢的甜，也有沙漠的风——现在，还有你的目光。'; } }
        ],
        koa: [
          { ico: '🦈', t: '来信：海洋巡游者', body: function (s) { return 'Koa 最新定位在 <b>' + s.lat + s.latH + ', ' + s.lon + s.lonH + '</b>（' + s.freshTxt + '）。大白鲨是海洋里不知疲倦的巡游者——它沿着水温适宜的海域移动，捕食海豹、金枪鱼和海鸟。它已巡游 <b>' + s.totalKm + ' 公里</b>，与你相伴 ' + s.days + ' 天。'; } },
          { ico: '🌡️', t: '来信：它喜欢的水温', body: function (s) { return '大白鲨偏爱 12–24°C 的海水——太冷就去热带，太热就向高纬走。它最新一次定位：' + s.fmtD + '，在 <b>' + s.lat + s.latH + ', ' + s.lon + s.lonH + '</b> 附近。它可以下潜上千米，再回到海面晒太阳。'; } },
          { ico: '🌊', t: '来信：深蓝里的它', body: function (s) { return '此刻的 Koa 在 <b>' + s.lat + s.latH + ', ' + s.lon + s.lonH + '</b> 附近的深蓝里巡游。它已经陪你走了 <b>' + s.totalKm + ' 公里</b> 的海洋。大海辽阔，但它的旅途里，始终有一道目光跟着。'; } },
          { ico: '💌', t: '来信：守护者的第' + 'N' + '天', body: function (s) { return '你守护 Koa 第 <b>' + s.days + '</b> 天了。它不会上岸，不会鸣叫，但每一次浮出水面，都是它在跟你打招呼。'; } }
        ],
        _default: [
          { ico: '📬', t: '来信：它还在路上', body: function (s) { return '它最新足迹在 <b>' + s.lat + s.latH + ', ' + s.lon + s.lonH + '</b>（' + s.freshTxt + '）。已累计移动 <b>' + s.totalKm + ' 公里</b>，与你相伴 ' + s.days + ' 天。'; } }
        ]
      };
      function genLiveLetter(s) {
        var pool = liveLetters[animalId] || liveLetters._default;
        if (!pool || !pool.length) return null;
        var tpl = _rnd(pool);
        try { return { ico: tpl.ico, t: tpl.t.replace(/'N'/, ''), body: tpl.body(s) }; }
        catch (e) { return null; }
      }
'''
assert ANCHOR1 in c, 'customLetters锚点未找到'
c = c.replace(ANCHOR1, LIVE_JS + ANCHOR1, 1)
print('liveLetters已插入')

# ============ 2. 插入今日来信渲染（在 var html = ''; 前） ============
ANCHOR2 = "      var html = '';"
LIVE_RENDER = r'''      // 📬 今日来信（领养后显示，随机模板+真实数据）
      var liveHtml = '';
      if (days >= 0 && pts && pts.length) {
        try {
          var lpt = pts[pts.length - 1];
          var lts = timestamps[timestamps.length - 1];
          var liveS = {
            lat: _sfmt(lpt[1]), latH: lpt[1] >= 0 ? '°N' : '°S',
            lon: _sfmt(lpt[0]), lonH: lpt[0] >= 0 ? '°E' : '°W',
            totalKm: Math.round(totalKm),
            days: days,
            freshTxt: fresh,
            fmtD: fmtD(lts)
          };
          var lv = genLiveLetter(liveS);
          if (lv) liveHtml = '<div class="letter-item live"><div class="letter-head"><span>' + lv.ico + ' ' + lv.t + '</span><span class="letter-st">📬 今日来信</span></div><div class="letter-body">' + lv.body + '</div></div>';
        } catch (e) {}
      }
'''
assert ANCHOR2 in c, 'html=锚点未找到'
c = c.replace(ANCHOR2, LIVE_RENDER + ANCHOR2, 1)
print('今日来信渲染已插入')

# ============ 3. 插入 Noé 专属信（customLetters 内 turtle 之后） ============
ANCHOR3 = "        ]\n      };\n      var letters = customLetters[animalId] || defaultLetters;"
NOE_LETTERS = r'''        ],
        noe: [
          { d: 0, t: '初遇之信', ico: '💌', body: '亲爱的<b>' + name + '</b>：<br>从今天起，你就是 Noé 的守护者了。此刻它正在<b>西班牙东部</b>（40.9°N, 1.5°W）上空——秋天到了，它正沿着古老的路线向南，跟着热气流一段一段地飞向西非。为了和你相遇，它已经独自飞了 <b>' + Math.round(totalKm) + ' 公里</b>，往返欧洲与非洲整整五年。从今天起，每一公里都有你的目光。' },
          { d: 1, t: '萨尔堡的夏天', ico: '🌾', body: '2021年6月29日，法国东北部的萨尔堡（48.99°N, 7.05°E），科学家给一只年轻的白鹳戴上了GPS追踪器——它叫 Noé。它当时正站在麦田边的电线上，红嘴红腿，翅膀尖是黑色的。它不知道这个小小的背包会记录下它此后五年的每一次飞翔。' },
          { d: 3, t: '屋顶上的家', ico: '🏠', body: '白鹳喜欢住在屋顶上。Noé 在法国阿尔萨斯找到了一户人家的烟囱顶，把巢搭在那里——大得像个草垛。每年夏天它都回来修补：叼来树枝、麦秆、碎布，一点点添上去。当地人看到白鹳在屋顶筑巢，会当作好运气。' },
          { d: 7, t: '哒哒哒', ico: '🗣️', body: '白鹳几乎不叫——它们用喙说话。Noé 把上下喙快速敲击，发出哒哒哒哒的声响，像有人在敲木鱼。这是它在说：我回来了；这也是它在说：这片屋顶是我的。你永远不会忘记第一次听到白鹳敲喙的声音。' },
          { d: 10, t: '第一次远行', ico: '✈️', body: '2021年9月，秋天的风从北方吹来。Noé 站在巢边，朝着南方看了很久。然后它张开两米宽的翅膀，顺着第一股上升热气流盘旋升高——越来越高，直到变成天空里的一个小点。它就这样，开始了生命里第一次跨国迁徙。' },
          { d: 14, t: '直布罗陀海峡', ico: '🌊', body: '白鹳的迁徙路线要经过直布罗陀海峡——那里是欧洲与非洲最近的地方。Noé 在海峡上空盘旋，等待热气流把它托到足够高的地方，然后一鼓作气滑翔过海。海面上没有可以停歇的地方，它只能相信自己的翅膀。' },
          { d: 21, t: '摩洛哥的冬天', ico: '🌴', body: '翻过地中海，Noé 来到了摩洛哥（34.3°N, 6.6°W）。那里的冬天没有雪，只有暖阳和田野。它和成群的同伴在农田里散步，长喙一探一探地啄食昆虫和蛙。这是它第一次知道：原来冬天也可以这么暖和。' },
          { d: 30, t: '撒哈拉的边缘', ico: '🏜️', body: 'Noé 最南到过北纬 34.2°——西非撒哈拉沙漠的南缘。那里有绿洲、有湿地，是许多白鹳的越冬地。五年的追踪里，它在这片土地上来回往返，累计飞过 <b>' + Math.round(totalKm) + ' 公里</b>，最北回到法国阿尔萨斯，最南抵达西非。' },
          { d: 45, t: '春天向北', ico: '🌸', body: '每年2到4月，白鹳体内的生物钟开始倒数。Noé 在摩洛哥的田野里梳好羽毛，然后展开翅膀——向北。它认得回家的路：先沿海岸线飞，再翻过直布罗陀，最后沿着河谷一路回到阿尔萨斯。' },
          { d: 60, t: '热气流学校', ico: '🌬️', body: '白鹳是滑翔冠军——它们几乎不扇翅膀。Noé 找到一股上升热气流，就绕着圈盘旋，像坐电梯一样升到几百米高，然后平展翅膀向南方滑翔几公里，再找下一股。一天能这样飞几百公里，却几乎不费力气。' },
          { d: 90, t: '五年的路', ico: '🧭', body: '从2021年到今天，Noé 往返欧洲与非洲，累计飞行超过 <b>' + Math.round(totalKm) + ' 公里</b>——足够绕地球半圈还多。它见过直布罗陀的海雾、摩洛哥的麦田、撒哈拉的落日，也记得阿尔萨斯屋顶上的每一根树枝。' },
          { d: 100, t: '与你的约定', ico: '💞', body: '亲爱的<b>' + name + '</b>：<br>一百天了。Noé 在天空里的每一公里，都有你的注视；它停下的每一片田野，都有你的名字。五年的迁徙，它把故事讲给了风——而风，讲给了路过的人。现在，轮到你了。' }
        ]
      };
      var letters = customLetters[animalId] || defaultLetters;'''
assert ANCHOR3 in c, 'customLetters尾部锚点未找到'
c = c.replace(ANCHOR3, NOE_LETTERS, 1)
print('Noé专属信已插入')

open(P, 'w', encoding='utf-8', newline='\n').write(c)
print('OK')
