# -*- coding: utf-8 -*-
"""轨迹视觉升级：动物专属主题色 + 起点emoji标记 + 渐变轨迹 + 终点脉冲"""
P = 'app/static/animal.html'
c = open(P, encoding='utf-8').read()
orig = c

# ===== 1. renderTrack 开头插入主题表 + 起点标记 =====
anchor = """  function renderTrack(smooth, style) {
    clearTrackLayers();
    if (!map || smooth.length < 2) return;
    """
inject = """  function renderTrack(smooth, style) {
    clearTrackLayers();
    if (!map || smooth.length < 2) return;
    
    // ===== 0. 动物专属主题（每只动物有自己的颜色与图标） =====
    var animalThemes = {
      noe:         { main: '#10B981', dark: '#047857', light: '#A7F3D0', bg: '#E2E8F0', emoji: '🕊️' },
      turtle:      { main: '#0EA5E9', dark: '#0369A1', light: '#BAE6FD', bg: '#E0F2FE', emoji: '🐢' },
      redkite:     { main: '#F59E0B', dark: '#B45309', light: '#FDE68A', bg: '#FEF3C7', emoji: '🪁' },
      honeybuzzard:{ main: '#F97316', dark: '#C2410C', light: '#FED7AA', bg: '#FFEDD5', emoji: '🐝' },
      herringgull: { main: '#64748B', dark: '#334155', light: '#CBD5E1', bg: '#F1F5F9', emoji: '🕊️' },
      koa:         { main: '#2563EB', dark: '#1E40AF', light: '#BFDBFE', bg: '#DBEAFE', emoji: '🦈' }
    };
    var th = animalThemes[animalId] || animalThemes.noe;
    
    // 起点标记：旅程从这里开始（动物图标）
    var sMark = L.marker(smooth[0], {
      icon: L.divIcon({
        className: '',
        html: '<div style="width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,' + th.light + ',' + th.main + ');border:3px solid #fff;box-shadow:0 3px 12px ' + th.main + '66;display:flex;align-items:center;justify-content:center;font-size:17px;">' + th.emoji + '</div>',
        iconSize: [36, 36], iconAnchor: [18, 18]
      })
    }).addTo(map);
    trackLayers.push(sMark);
    """
assert anchor in c, 'renderTrack锚点未找到'
c = c.replace(anchor, inject)

# ===== 2. ant样式换主题色（默认样式，视觉提升最大） =====
old_ant = """    if (style === 'ant') {
      // 淡色底图轨迹（已完成的部分）
      var trailBg = L.polyline(smooth, { color: '#E2E8F0', weight: 5, opacity: 0.55, dashArray: null }).addTo(map);
      trackLayers.push(trailBg);
      // 主轨迹：从起点到当前播放位置，翠绿渐变+发光
      var curEnd = Math.max(2, idx + 1);
      var drawn = smooth.slice(0, curEnd);
      var glow = L.polyline(drawn, { color: '#34D399', weight: 15, opacity: 0.22 }).addTo(map);
      trackLayers.push(glow);
      var main = L.polyline(drawn, { color: '#10B981', weight: 6, opacity: 1 }).addTo(map);
      trackLayers.push(main);
      // 已走过的轨迹（主色覆盖）
      if (idx < smooth.length - 1) {
        var ahead = L.polyline(smooth.slice(curEnd), { color: '#A7F3D0', weight: 1.5, opacity: 0.25, dashArray: '4,6' }).addTo(map);
        trackLayers.push(ahead);
      }
      // 当前播放位置发光点
      var curPos = smooth[curEnd - 1];
      var halo = L.circleMarker(curPos, { radius: 10, fillColor: '#34D399', color: '#fff', weight: 2, fillOpacity: 0.35 }).addTo(map);
      trackLayers.push(halo);
      var core = L.circleMarker(curPos, { radius: 5, fillColor: '#10B981', color: '#fff', weight: 2, fillOpacity: 1 }).addTo(map);
      trackLayers.push(core);
    }"""
new_ant = """    if (style === 'ant') {
      // 淡色底图轨迹（已完成的部分）
      var trailBg = L.polyline(smooth, { color: th.bg, weight: 5, opacity: 0.6, dashArray: null }).addTo(map);
      trackLayers.push(trailBg);
      // 主轨迹：从起点到当前播放位置，主题色渐变+发光
      var curEnd = Math.max(2, idx + 1);
      var drawn = smooth.slice(0, curEnd);
      var glow = L.polyline(drawn, { color: th.main, weight: 15, opacity: 0.22 }).addTo(map);
      trackLayers.push(glow);
      // 渐变主轨：按时间从浅到深（起点亮 → 当前位置深）
      var segN = 6;
      for (var si2 = 0; si2 < segN; si2++) {
        var sStart = Math.floor(si2 * drawn.length / segN);
        var sEnd = Math.max(sStart + 1, Math.floor((si2 + 1) * drawn.length / segN));
        var seg = L.polyline(drawn.slice(sStart, sEnd), {
          color: si2 >= segN - 1 ? th.main : th.light,
          weight: si2 >= segN - 1 ? 6 : 4.5,
          opacity: 0.35 + (si2 / segN) * 0.65
        }).addTo(map);
        trackLayers.push(seg);
      }
      // 已走过的轨迹（主色覆盖）
      if (idx < smooth.length - 1) {
        var ahead = L.polyline(smooth.slice(curEnd), { color: th.light, weight: 1.5, opacity: 0.25, dashArray: '4,6' }).addTo(map);
        trackLayers.push(ahead);
      }
      // 当前播放位置：脉冲呼吸发光点（动物正在这里！）
      var curPos = smooth[curEnd - 1];
      var halo = L.circleMarker(curPos, { radius: 11, fillColor: th.main, color: '#fff', weight: 2, fillOpacity: 0.3, className: 'pulse-dot' }).addTo(map);
      trackLayers.push(halo);
      var core = L.circleMarker(curPos, { radius: 5, fillColor: th.dark, color: '#fff', weight: 2, fillOpacity: 1 }).addTo(map);
      trackLayers.push(core);
    }"""
assert old_ant in c, 'ant样式未找到'
c = c.replace(old_ant, new_ant)

# ===== 3. dots 起终点标记换主题emoji =====
old_dots_s = """      var sDot = L.marker(smooth, {
        icon: L.divIcon({ className: '', html: '<div style="background:linear-gradient(135deg,#3B82F6,#1D4ED8);color:#fff;width:38px;height:38px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px;border:3px solid #fff;box-shadow:0 3px 10px rgba(59,130,246,.5);">起</div>', iconSize: [38,38], iconAnchor: [19,19] })
      }).addTo(map);"""
new_dots_s = """      var sDot = L.marker(smooth, {
        icon: L.divIcon({ className: '', html: '<div style="background:linear-gradient(135deg,' + th.light + ',' + th.main + ');width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:17px;border:3px solid #fff;box-shadow:0 3px 10px ' + th.main + '66;">' + th.emoji + '</div>', iconSize: [36,36], iconAnchor: [18,18] })
      }).addTo(map);"""
assert old_dots_s in c, 'dots起点未找到'
c = c.replace(old_dots_s, new_dots_s)

old_dots_e = """      var eDot = L.marker(smooth[smooth.length-1], {
        icon: L.divIcon({ className: '', html: '<div style="background:linear-gradient(135deg,#EF4444,#B91C1C);color:#fff;width:38px;height:38px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px;border:3px solid #fff;box-shadow:0 3px 10px rgba(239,68,68,.5);">终</div>', iconSize: [38,38], iconAnchor: [19,19] })
      }).addTo(map);"""
new_dots_e = """      var eDot = L.marker(smooth[smooth.length-1], {
        icon: L.divIcon({ className: '', html: '<div style="background:linear-gradient(135deg,' + th.main + ',' + th.dark + ');color:#fff;width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:17px;border:3px solid #fff;box-shadow:0 3px 10px ' + th.main + '66;">' + th.emoji + '</div>', iconSize: [36,36], iconAnchor: [18,18] })
      }).addTo(map);"""
assert old_dots_e in c, 'dots终点未找到'
c = c.replace(old_dots_e, new_dots_e)

# ===== 4. arrow 换主题色 =====
old_arrow = """    else if (style === 'arrow') {
      // 底图淡色线
      var aBg = L.polyline(smooth, { color: '#DBEAFE', weight: 7, opacity: 0.6 }).addTo(map);
      trackLayers.push(aBg);
      // 主体导航线
      var aMain = L.polyline(smooth, { color: '#1D4ED8', weight: 5, opacity: 0.9 }).addTo(map);
      trackLayers.push(aMain);"""
new_arrow = """    else if (style === 'arrow') {
      // 底图淡色线
      var aBg = L.polyline(smooth, { color: th.bg, weight: 7, opacity: 0.6 }).addTo(map);
      trackLayers.push(aBg);
      // 主体导航线
      var aMain = L.polyline(smooth, { color: th.main, weight: 5, opacity: 0.9 }).addTo(map);
      trackLayers.push(aMain);"""
assert old_arrow in c, 'arrow未找到'
c = c.replace(old_arrow, new_arrow)

# 箭头三角形也换色
old_arr2 = "html: '<div style=\"transform:rotate(' + angle + 'deg);width:0;height:0;border-left:10px solid transparent;border-right:10px solid transparent;border-bottom:22px solid #1D4ED8;filter:drop-shadow(0 0 5px rgba(29,78,216,.9));\"></div>'"
new_arr2 = "html: '<div style=\"transform:rotate(' + angle + 'deg);width:0;height:0;border-left:10px solid transparent;border-right:10px solid transparent;border-bottom:22px solid ' + th.main + ';filter:drop-shadow(0 0 5px ' + th.main + ';\"></div>'"
assert old_arr2 in c, '箭头未找到'
c = c.replace(old_arr2, new_arr2)

old_aCur = "var aCur = L.circleMarker(smooth[smooth.length-1], { radius: 9, fillColor: '#1D4ED8', color: '#fff', weight: 3, fillOpacity: 1 }).addTo(map);"
new_aCur = "var aCur = L.circleMarker(smooth[smooth.length-1], { radius: 9, fillColor: th.main, color: '#fff', weight: 3, fillOpacity: 1, className: 'pulse-dot' }).addTo(map);"
assert old_aCur in c, '当前位置标记未找到'
c = c.replace(old_aCur, new_aCur)

# ===== 5. CSS 脉冲动画（在 .tab-bar 样式前插入） =====
css_anchor = "  .tab-bar {"
pulse_css = """  .pulse-dot circle {
    animation: pulseA 2.2s ease-in-out infinite;
    transform-origin: center;
  }
  @keyframes pulseA {
    0%, 100% { opacity: .95; }
    50% { opacity: .35; }
  }
  .tab-bar {"""
assert css_anchor in c, 'CSS锚点未找到'
c = c.replace(css_anchor, pulse_css, 1)

open(P, 'w', encoding='utf-8').write(c)
print('✅ 轨迹视觉升级完成')
print('长度:', len(orig), '→', len(c))
print('主题表:', c.count('animalThemes'))
print('起点标记:', c.count('var sMark'))
print('脉冲CSS:', c.count('pulseA'))
print('渐变主轨:', c.count('segN'))
