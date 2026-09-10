# -*- coding: utf-8 -*-
"""PWA推送落地(1b/3)：VAPID密钥(cryptography) + sw.js推送版"""
import sys, os, json, base64
sys.stdout.reconfigure(encoding='utf-8')

# ---------- 2. VAPID 密钥（cryptography 生成 P-256） ----------
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

vp = os.path.join('data', 'vapid.json')
if not os.path.exists(vp):
    priv = ec.generate_private_key(ec.SECP256R1())
    priv_pem = priv.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    ).decode()
    pub_raw = priv.public_key().public_bytes(
        serialization.Encoding.X962,
        serialization.PublicFormat.UncompressedPoint,
    )
    pub_b64 = base64.urlsafe_b64encode(pub_raw).rstrip(b'=').decode()
    d = {
        "private_key": priv_pem,
        "public_key": pub_b64,
        "subject": "mailto:admin@animal-bracelet.onrender.com",
    }
    with open(vp, 'w', encoding='utf-8') as f:
        json.dump(d, f, indent=2)
    print('2. VAPID 已生成 →', vp, '| 公钥前20:', pub_b64[:20])
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
