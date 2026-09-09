# -*- coding: utf-8 -*-
"""轨迹升级 第二部分：dots/arrow换主题色 + 脉冲CSS"""
P = 'app/static/animal.html'
c = open(P, encoding='utf-8').read()

# dots 起点标记（只换html字符串）
old_s = "html: '<div style=\"background:linear-gradient(135deg,#3B82F6,#1D4ED8);color:#fff;width:38px;height:38px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px;border:3px solid #fff;box-shadow:0 3px 10px rgba(59,130,246,.5);\">起</div>', iconSize: [38,38], iconAnchor: [19,19]"
new_s = "html: '<div style=\"background:linear-gradient(135deg,' + th.light + ',' + th.main + ');width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:17px;border:3px solid #fff;box-shadow:0 3px 10px ' + th.main + '66;\">' + th.emoji + '</div>', iconSize: [36,36], iconAnchor: [18,18]"
assert old_s in c, 'dots起点html未找到'
c = c.replace(old_s, new_s)

old_e = "html: '<div style=\"background:linear-gradient(135deg,#EF4444,#B91C1C);color:#fff;width:38px;height:38px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px;border:3px solid #fff;box-shadow:0 3px 10px rgba(239,68,68,.5);\">终</div>', iconSize: [38,38], iconAnchor: [19,19]"
new_e = "html: '<div style=\"background:linear-gradient(135deg,' + th.main + ',' + th.dark + ');color:#fff;width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:17px;border:3px solid #fff;box-shadow:0 3px 10px ' + th.main + '66;\">' + th.emoji + '</div>', iconSize: [36,36], iconAnchor: [18,18]"
assert old_e in c, 'dots终点html未找到'
c = c.replace(old_e, new_e)

# arrow 换主题色
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

old_arr2 = "border-bottom:22px solid #1D4ED8;filter:drop-shadow(0 0 5px rgba(29,78,216,.9));"
new_arr2 = "border-bottom:22px solid ' + th.main + ';filter:drop-shadow(0 0 5px ' + th.main + ';"
assert old_arr2 in c, '箭头未找到'
c = c.replace(old_arr2, new_arr2)

old_aCur = "var aCur = L.circleMarker(smooth[smooth.length-1], { radius: 9, fillColor: '#1D4ED8', color: '#fff', weight: 3, fillOpacity: 1 }).addTo(map);"
new_aCur = "var aCur = L.circleMarker(smooth[smooth.length-1], { radius: 9, fillColor: th.main, color: '#fff', weight: 3, fillOpacity: 1, className: 'pulse-dot' }).addTo(map);"
assert old_aCur in c, '当前位置标记未找到'
c = c.replace(old_aCur, new_aCur)

# 脉冲CSS（.tab-bar前插入）
css_anchor = "  .tab-bar {"
pulse_css = """  .pulse-dot circle {
    animation: pulseA 2.2s ease-in-out infinite;
  }
  @keyframes pulseA {
    0%, 100% { opacity: .95; }
    50% { opacity: .35; }
  }
  .tab-bar {"""
assert css_anchor in c, 'CSS锚点未找到'
c = c.replace(css_anchor, pulse_css, 1)

open(P, 'w', encoding='utf-8').write(c)
print('✅ 轨迹升级(2/2)完成')
print('脉冲CSS:', c.count('pulseA'))
print('dots起点emoji:', c.count("th.emoji"))
print('arrow主题色:', c.count('th.main'))
