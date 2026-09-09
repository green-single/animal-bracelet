/* 动物追踪手环 · Service Worker（清理版 v2）
 * 历史版本（v1）的错误缓存策略导致照片/页面被旧缓存钉死，加载不出来。
 * 本版本：安装即跳过等待，激活时清除全部缓存并注销自身，
 * 让网站回到"纯网络加载"模式（数据实时、照片永远最新）。
 * 注册代码保留在页面中，浏览器会自动拉取本文件并完成一次性清理。
 */
self.addEventListener('install', function () {
  self.skipWaiting();
});

self.addEventListener('activate', function (event) {
  event.waitUntil(
    caches.keys()
      .then(function (keys) {
        return Promise.all(keys.map(function (k) { return caches.delete(k); }));
      })
      .then(function () {
        // 清理完成后注销 Service Worker，恢复纯网络模式
        return self.registration.unregister();
      })
      .then(function () {
        // 通知所有打开的页面刷新，立即生效
        return self.clients.matchAll({ type: 'window' }).then(function (clients) {
          clients.forEach(function (client) { client.navigate(client.url); });
        });
      })
  );
});

// 清理期间不拦截任何请求，全部走网络
self.addEventListener('fetch', function () {});
