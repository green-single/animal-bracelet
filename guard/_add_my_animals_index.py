# -*- coding: utf-8 -*-
"""index.html：加「我的动物」聚合入口"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
P = 'app/static/index.html'
c = open(P, encoding='utf-8', newline='').read()
c = c.replace('\r\n', '\n')

# 1. header 加按钮
OLD_HEADER = """<header>
  <div class="logo">爪</div>
  <div class="brand">动物追踪手环<small>扫码领养一只真实迁徙的动物</small></div>
</header>"""
NEW_HEADER = """<header>
  <div class="logo">爪</div>
  <div class="brand">动物追踪手环<small>扫码领养一只真实迁徙的动物</small></div>
  <button id="myAnimalsBtn" type="button" style="display:none;margin-left:auto;background:#12796F;color:#fff;border:none;border-radius:20px;padding:8px 16px;font-size:14px;cursor:pointer;flex-shrink:0;">🐾 我的动物</button>
</header>"""
assert OLD_HEADER in c, 'header锚点未找到'
c = c.replace(OLD_HEADER, NEW_HEADER, 1)

# 2. 加面板HTML（body末尾，footer后）
OLD_FOOT = """<footer>
  动物追踪手环 · 让每一次迁徙都被看见<br>
  数据来源：Movebank CC0 · 照片：Wikimedia Commons<br>
  <a href="/animals">管理员入口</a>
</footer>"""
NEW_FOOT = OLD_FOOT + """

<!-- 我的动物面板 -->
<div id="myAnimalsPanel" style="display:none;position:fixed;top:64px;right:12px;z-index:9999;background:#fff;border:1px solid rgba(0,0,0,.08);border-radius:16px;box-shadow:0 12px 40px rgba(0,0,0,.18);width:300px;max-width:calc(100vw - 24px);padding:14px;font-family:'PingFang SC','Microsoft YaHei',sans-serif;">
  <div style="font-size:15px;font-weight:600;color:#1A1B1C;margin-bottom:10px;">🐾 我的动物</div>
  <div id="myAnimalsList"></div>
  <div style="margin-top:10px;font-size:12px;color:#6B7280;border-top:1px solid rgba(0,0,0,.06);padding-top:8px;">领养记录保存在本设备浏览器中，换设备需重新扫码</div>
</div>"""
assert OLD_FOOT in c, 'footer锚点未找到'
c = c.replace(OLD_FOOT, NEW_FOOT, 1)

# 3. 加JS（script 区）
OLD_JS = """<script>
// 输领养码查询动物"""
NEW_JS = """<script>
var ANIMALS = {
  turtle: 'Lumi · 欧斑鸠', noe: 'Noé · 白鹳', herringgull: 'Silver · 银鸥',
  redkite: 'Athos · 红鸢', honeybuzzard: 'Mel · 蜂鹰', koa: 'Koa · 大白鲨'
};
function collectMyAnimals() {
  var list = [];
  try {
    for (var i = 0; i < localStorage.length; i++) {
      var k = localStorage.key(i);
      if (k && k.indexOf('adopted_') === 0) {
        var id = k.slice(8);
        if (ANIMALS[id]) {
          var info = { id: id, name: ANIMALS[id] };
          try {
            var a = JSON.parse(localStorage.getItem(k) || 'null');
            if (a && a.nickname) info.nick = a.nickname;
            if (a && a.date) info.date = a.date;
          } catch (e) {}
          list.push(info);
        }
      }
    }
  } catch (e) {}
  return list;
}
function renderMyAnimals() {
  var list = collectMyAnimals();
  var btn = document.getElementById('myAnimalsBtn');
  if (!btn) return;
  if (list.length === 0) { btn.style.display = 'none'; return; }
  btn.style.display = 'block';
  var box = document.getElementById('myAnimalsList');
  if (!box) return;
  var html = '';
  list.forEach(function (m) {
    var days = '';
    if (m.date) {
      try { days = Math.max(1, Math.floor((Date.now() - new Date(m.date).getTime()) / 86400000)) + ' 天'; } catch (e) {}
    }
    html += '<a href="/animal/' + m.id + '" style="display:flex;align-items:center;gap:10px;padding:9px 8px;border-radius:10px;text-decoration:none;color:#1A1B1C;">' +
      '<span style="font-size:22px;">🐾</span>' +
      '<span style="flex:1;min-width:0;"><span style="display:block;font-size:14px;font-weight:600;">' + m.name + '</span>' +
      (m.nick ? '<span style="display:block;font-size:12px;color:#6B7280;">守护者：' + m.nick + '</span>' : '') + '</span>' +
      (days ? '<span style="font-size:12px;color:#12796F;flex-shrink:0;">相伴 ' + days + '</span>' : '') + '</a>';
  });
  box.innerHTML = html;
}
document.addEventListener('DOMContentLoaded', function () {
  renderMyAnimals();
  var btn = document.getElementById('myAnimalsBtn');
  var panel = document.getElementById('myAnimalsPanel');
  if (btn && panel) {
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      renderMyAnimals();
      panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
    });
    document.addEventListener('click', function (e) {
      if (!panel.contains(e.target) && e.target !== btn) panel.style.display = 'none';
    });
  }
});
</script>
<script>
// 输领养码查询动物"""
assert OLD_JS in c, 'js锚点未找到'
c = c.replace(OLD_JS, NEW_JS, 1)

open(P, 'w', encoding='utf-8', newline='\n').write(c)
print('index.html 已加「我的动物」入口')
