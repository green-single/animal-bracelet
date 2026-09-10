# -*- coding: utf-8 -*-
"""PWA推送落地(3/3)：animal.html + index.html 前端"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

# ---------- animal.html ----------
P = 'app/static/animal.html'
c = open(P, encoding='utf-8', newline='').read()
c = c.replace('\r\n', '\n')

# 1. 替换"清除SW"代码段 → 注册SW
old_clear = """// 彻底清除Service Worker与缓存（防止旧版SW拦截照片请求）
if ('serviceWorker' in navigator) {
  try {
    navigator.serviceWorker.getRegistrations().then(function(regs) {
      regs.forEach(function(r) { r.unregister(); });
    });
  } catch(e) {}
}
if ('caches' in window) {
  try {
    caches.keys().then(function(keys) {
      keys.forEach(function(k) { caches.delete(k); });
    });
  } catch(e) {}
}"""
new_clear = """// 注册 Service Worker（推送通知用；纯网络模式，不缓存页面/照片）
if ('serviceWorker' in navigator) {
  try {
    navigator.serviceWorker.register('/sw.js').catch(function() {});
  } catch(e) {}
}"""
assert old_clear in c, 'animal.html 清除SW段未找到'
c = c.replace(old_clear, new_clear, 1)
print('a1. animal.html SW注册替换OK')

# 2. header 加推送按钮（codeGo 后）
old_btn = '<button id="scanBtn" type="button" title="扫手环上的二维码">📷 扫码</button>'
new_btn = old_btn + '\n    <button id="pushBtn" type="button" title="有新足迹时通知我">🔔</button>'
assert old_btn in c, 'scanBtn未找到'
c = c.replace(old_btn, new_btn, 1)
print('a2. animal.html 推送按钮已加')

# 3. body 末尾加推送逻辑
PUSH_JS = """
<script>
(function () {
  // 🔔 推送提醒（订阅制：谁开启，新足迹就推给谁）
  var btn = document.getElementById('pushBtn');
  if (!btn) return;
  if (!('serviceWorker' in navigator) || !('PushManager' in window) || !('Notification' in window)) {
    btn.style.display = 'none';
    return;
  }
  var animalId = decodeURIComponent((location.pathname.match(/\\/animal\\/([^\\/]+)/) || [, ''])[1] || '');
  function b64toU8(b64) {
    var raw = atob(b64);
    var u8 = new Uint8Array(raw.length);
    for (var i = 0; i < raw.length; i++) u8[i] = raw.charCodeAt(i);
    return u8;
  }
  function setOn(on) {
    if (on) { btn.classList.add('on'); btn.title = '已开启提醒（点击关闭）'; }
    else { btn.classList.remove('on'); btn.title = '有新足迹时通知我'; }
  }
  // 初始状态
  try {
    navigator.serviceWorker.getRegistration().then(function (reg) {
      if (reg && reg.pushManager) return reg.pushManager.getSubscription();
    }).then(function (sub) { setOn(!!sub); }).catch(function () {});
  } catch (e) {}
  btn.onclick = function () {
    if (btn.classList.contains('on')) {
      navigator.serviceWorker.getRegistration().then(function (reg) {
        if (reg && reg.pushManager) return reg.pushManager.getSubscription();
      }).then(function (sub) {
        if (sub) return sub.unsubscribe();
      }).then(function () { setOn(false); }).catch(function () {});
      return;
    }
    Notification.requestPermission().then(function (perm) {
      if (perm !== 'granted') { alert('请先允许通知权限，才能收到它的新足迹提醒'); return; }
      var pubKey = null;
      return fetch('/api/push/vapid-public-key').then(function (r) { return r.json(); }).then(function (d) { pubKey = d.public_key; })
        .then(function () { return navigator.serviceWorker.register('/sw.js'); })
        .then(function (reg) { return reg.pushManager.subscribe({ userVisibleOnly: true, applicationServerKey: b64toU8(pubKey) }); })
        .then(function (sub) {
          var p256dh = sub.getKey('p256dh') ? btoa(String.fromCharCode.apply(null, new Uint8Array(sub.getKey('p256dh')))) : '';
          var auth = sub.getKey('auth') ? btoa(String.fromCharCode.apply(null, new Uint8Array(sub.getKey('auth')))) : '';
          return fetch('/api/push/subscribe', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ animal_id: animalId, endpoint: sub.endpoint, p256dh: p256dh, auth: auth }) });
        })
        .then(function () { setOn(true); })
        .catch(function (e) { console.log('push err', e); });
    });
  };
})();
</script>
"""
if 'id="pushBtn"' in c and 'pushSubscribe' not in c:
    c = c.replace('</body>', PUSH_JS + '\n</body>', 1)
    print('a3. animal.html 推送逻辑已加')

open(P, 'w', encoding='utf-8', newline='\n').write(c)
print('animal.html OK | pushBtn:', c.count('pushBtn'), '| sw.js注册:', c.count("register('/sw.js')"))

# ---------- index.html ----------
P2 = 'app/static/index.html'
c2 = open(P2, encoding='utf-8', newline='').read()
c2 = c2.replace('\r\n', '\n')
if 'unregister()' in c2:
    # 找清除段（index.html的SW清除代码）
    import re
    # 替换所有 unregister 相关段
    old2 = re.search(r"// 彻底清除Service Worker与缓存.*?caches\.delete\(k\);[\s\S]*?\}\s*\}", c2, re.S)
    if old2:
        c2 = c2[:old2.start()] + "// 注册 Service Worker（推送通知用；纯网络模式）\nif ('serviceWorker' in navigator) {\n  try {\n    navigator.serviceWorker.register('/sw.js').catch(function() {});\n  } catch(e) {}\n}" + c2[old2.end():]
        print('b1. index.html SW清除段替换OK')
    else:
        # 兜底：逐行删 unregister 相关
        lines = c2.split('\n')
        out = []
        skip = False
        for l in lines:
            if '彻底清除Service Worker' in l:
                skip = True
            if skip and 'caches.delete' in l:
                skip = False
                out.append("// 注册 Service Worker（推送通知用；纯网络模式）\nif ('serviceWorker' in navigator) { try { navigator.serviceWorker.register('/sw.js').catch(function() {}); } catch(e) {} }")
                continue
            if not skip:
                out.append(l)
        c2 = '\n'.join(out)
        print('b1. index.html 行级替换OK')
open(P2, 'w', encoding='utf-8', newline='\n').write(c2)
print('index.html OK | unregister剩:', c2.count('unregister()'), '| sw注册:', c2.count("register('/sw.js')"))
