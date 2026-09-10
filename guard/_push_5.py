# -*- coding: utf-8 -*-
"""推送兜底：latest轻量接口 + 页面轮询通知"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

# ---------- 1. main.py 加 /api/animal/{id}/latest ----------
P = 'app/main.py'
c = open(P, encoding='utf-8', newline='').read()
c = c.replace('\r\n', '\n')

anchor = '@app.get("/api/animal/{animal_id}")'
latest = '''@app.get("/api/animal/{animal_id}/latest")
def api_animal_latest(animal_id: str):
    """轻量接口：只返回动物名 + 最新定位时间（页面轮询用，避免全量下载）"""
    conn = database.get_conn()
    row = conn.execute("SELECT name FROM animals WHERE id=?", (animal_id,)).fetchone()
    if row is None:
        conn.close()
        raise HTTPException(status_code=404, detail="动物不存在")
    p = conn.execute(
        "SELECT ts, lat, lon FROM track_points WHERE animal_id=? ORDER BY ts DESC LIMIT 1", (animal_id,)
    ).fetchone()
    conn.close()
    return {"name": row["name"], "latest_ts": p["ts"] if p else None, "lat": p["lat"] if p else None, "lon": p["lon"] if p else None}


'''
assert anchor in c, 'api_animal锚点未找到'
c = c.replace(anchor, latest + anchor, 1)
open(P, 'w', encoding='utf-8', newline='\n').write(c)
print('main.py latest接口已加')

# ---------- 2. animal.html 加页面轮询兜底 ----------
P2 = 'app/static/animal.html'
c2 = open(P2, encoding='utf-8', newline='').read()
c2 = c2.replace('\r\n', '\n')

POLL_JS = """
<script>
(function () {
  // 页面内兜底提醒（国内直连可用，不依赖系统推送服务）：网页开着时每5分钟检查新足迹
  if (!('Notification' in window)) return;
  var animalId = decodeURIComponent((location.pathname.match(/\\/animal\\/([^\\/]+)/) || [, ''])[1] || '');
  if (!animalId) return;
  var lastTs = null;
  function checkUpdate() {
    fetch('/api/animal/' + encodeURIComponent(animalId) + '/latest')
      .then(function (r) { return r.json(); })
      .then(function (d) {
        var ts = d.latest_ts;
        if (ts && lastTs && ts !== lastTs && Notification.permission === 'granted') {
          try {
            var n = new Notification('🐾 ' + (d.name || '它') + ' 有了新足迹', {
              body: '最新定位：' + (d.lat != null ? d.lat.toFixed(2) + '°N, ' + d.lon.toFixed(2) + '°E' : '新坐标') + '，点开看看',
              icon: '/static/icons/icon-192.png',
            });
            n.onclick = function () { window.focus(); window.scrollTo(0, 0); };
          } catch (e) {}
        }
        lastTs = ts || lastTs;
      }).catch(function () {});
  }
  if (Notification.permission === 'granted') {
    checkUpdate();
    setInterval(checkUpdate, 300000);
  }
})();
</script>
"""
if '页面内兜底提醒' not in c2:
    c2 = c2.replace('</body>', POLL_JS + '\n</body>', 1)
    print('animal.html 页面轮询兜底已加')
open(P2, 'w', encoding='utf-8', newline='\n').write(c2)
print('OK')
