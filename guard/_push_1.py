# -*- coding: utf-8 -*-
"""PWA推送落地(1/3)：push_subs表 + VAPID密钥 + sw.js推送版"""
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')

# ---------- 1. database.py 加 push_subs 表 ----------
P1 = 'app/database.py'
c1 = open(P1, encoding='utf-8', newline='').read()
if 'push_subs' not in c1:
    add = """
CREATE TABLE IF NOT EXISTS push_subs (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    animal_id  TEXT NOT NULL DEFAULT '',
    endpoint   TEXT NOT NULL UNIQUE,
    p256dh     TEXT NOT NULL,
    auth       TEXT NOT NULL,
    created_at TEXT DEFAULT (datetime('now'))
);
"""
    anchor = "CREATE INDEX IF NOT EXISTS idx_track_animal ON track_points(animal_id);"
    assert anchor in c1, 'database锚点未找到'
    c1 = c1.replace(anchor, anchor + add, 1)
    open(P1, 'w', encoding='utf-8', newline='\n').write(c1)
    print('1. database.py push_subs表 已加')
else:
    print('1. push_subs已存在')

# ---------- 2. VAPID 密钥 ----------
from pywebpush import generate_vapid_keys
vp = os.path.join('data', 'vapid.json')
if not os.path.exists(vp):
    v = generate_vapid_keys()
    d = {
        "private_key": v["private_key"],
        "public_key": v["public_key"],
        "subject": "mailto:admin@animal-bracelet.onrender.com",
    }
    with open(vp, 'w', encoding='utf-8') as f:
        json.dump(d, f, indent=2)
    print('2. VAPID 已生成 →', vp, '| 公钥前20:', v["public_key"][:20])
else:
    print('2. VAPID 已存在')

# ---------- 3. sw.js 推送版 ----------
SW = """/* 动物追踪手环 · Service Worker v3（推送版）
 * 原则：纯网络模式（不缓存任何响应，避免照片被旧缓存钉死）；
 *       只负责 Web Push 推送通知。
 */
self.addEventListener('install', function (event) {
  self.skipWaiting();
});

self.addEventListener('activate', function (event) {
  event.waitUntil(
    caches.keys()
      .then(function (keys) { return Promise.all(keys.map(function (k) { return caches.delete(k); })); })
      .then(function () { return self.clients.claim(); })
  );
});

// 纯网络：不拦截任何请求
self.addEventListener('fetch', function () {});

// 收到推送 → 显示通知
self.addEventListener('push', function (event) {
  var data = {};
  try { data = event.data.json(); } catch (err) {}
  var options = {
    body: data.body || '它刚刚留下了一个新的足迹，快来看看',
    icon: data.icon || '/static/icons/icon-192.png',
    badge: data.icon || '/static/icons/icon-192.png',
    vibrate: [100, 50, 100],
    data: { url: data.url || '/' }
  };
  event.waitUntil(self.registration.showNotification(data.title || '🐾 它有了新足迹', options));
});

// 点击通知 → 打开对应动物页
self.addEventListener('notificationclick', function (event) {
  event.notification.close();
  var url = (event.notification.data && event.notification.data.url) || '/';
  event.waitUntil(
    self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then(function (list) {
      for (var i = 0; i < list.length; i++) {
        if ('focus' in list[i]) { list[i].navigate(url); list[i].focus(); return; }
      }
      return self.clients.openWindow(url);
    })
  );
});
"""
open('app/static/sw.js', 'w', encoding='utf-8', newline='\n').write(SW)
print('3. sw.js 推送版 已重写')
