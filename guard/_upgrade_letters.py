# -*- coding: utf-8 -*-
"""信升级：加初遇信(第0天) + 真实轨迹距离替换随机数"""
P = 'app/static/animal.html'
NL = chr(10)
c = open(P, encoding='utf-8').read()
lines = c.split(NL)

# ---------- 1. 在letters定义前插入真实距离计算 ----------
old_letters = "      var letters = ["
new_dist = """      // 真实累计飞行距离（haversine）
      var totalKm = 0;
      if (points && points.length > 1) {
        var R_ = 6371;
        for (var pi_ = 1; pi_ < points.length; pi_++) {
          var p1_ = points[pi_ - 1], p2_ = points[pi_];
          var dLat_ = (p2_[1] - p1_[1]) * Math.PI / 180;
          var dLon_ = (p2_[0] - p1_[0]) * Math.PI / 180;
          var a_ = Math.sin(dLat_ / 2) * Math.sin(dLat_ / 2) +
                   Math.cos(p1_[1] * Math.PI / 180) * Math.cos(p2_[1] * Math.PI / 180) *
                   Math.sin(dLon_ / 2) * Math.sin(dLon_ / 2);
          totalKm += R_ * 2 * Math.atan2(Math.sqrt(a_), Math.sqrt(1 - a_));
        }
      }
      var letters = ["""
assert old_letters in c, 'letters锚点未找到'
c = c.replace(old_letters, new_dist, 1)

# ---------- 2. 加初遇信（第0天） + 随机数改真实 ----------
old_random = "Math.round((a.region_label ? 1000 : 1000) * Math.random() + 3000)"
assert old_random in c, '随机数锚点未找到'
c = c.replace(old_random, "Math.round(totalKm)", 1)

old_letters_arr = """      var letters = [
        { d: 7, t: '第七夜的信', ico: '🌙', body: '亲爱的<b>' + name + '</b>：<br>整整七天了。"""
new_letters_arr = """      var letters = [
        { d: 0, t: '初遇之信', ico: '💌', body: '亲爱的<b>' + name + '</b>：<br>从今天起，你就是它的守护者了。它此刻在<b>' + (a.region_label || '远方') + '</b>，已经为你飞过了 <b>' + Math.round(totalKm) + ' 公里</b>。从今天起，每一公里都有你的目光。' },
        { d: 7, t: '第七夜的信', ico: '🌙', body: '亲爱的<b>' + name + '</b>：<br>整整七天了。"""
assert old_letters_arr in c, 'letters数组锚点未找到'
c = c.replace(old_letters_arr, new_letters_arr, 1)

# ---------- 3. 未领养时也显示初遇信的预告 ----------
old_locked = "html += '<div class=\"letter-item locked\"><div class=\"letter-head\"><span>' + L.ico + ' ' + L.t + '</span><span class=\"letter-st\">🔒 领养后解锁</span></div><div class=\"letter-body\">扫码领养它，这封信会在第 ' + L.d + ' 天送到你手上。</div></div>';"
new_locked = "html += '<div class=\"letter-item locked\"><div class=\"letter-head\"><span>' + L.ico + ' ' + L.t + '</span><span class=\"letter-st\">🔒 领养后解锁</span></div><div class=\"letter-body\">' + (L.d === 0 ? '扫码领养它，这封信会立刻送到你手上。' : '扫码领养它，这封信会在第 ' + L.d + ' 天送到你手上。') + '</div></div>';"
assert old_locked in c, 'locked锚点未找到'
c = c.replace(old_locked, new_locked, 1)

open(P, 'w', encoding='utf-8').write(c)
print('OK 信升级完成')
print('初遇信:', c.count("初遇之信"))
print('真实距离:', c.count('Math.round(totalKm)'))
print('随机数残留:', c.count('Math.random()'))
