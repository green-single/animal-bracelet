# -*- coding: utf-8 -*-
"""
动物追踪手环 · 后端服务
========================
启动：python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
或：  python run.py

接口：
  GET  /                   首页（demo 入口）
  GET  /c/{code}           扫码领养页（前端页面）
  GET  /animal/{id}        动物主页（前端页面）
  GET  /api/animals        全部动物列表（demo 用）
  GET  /api/claim/{code}   查询领养码状态（返回动物信息）
  POST /api/claim/{code}   执行领养（一码一次）
  GET  /api/animal/{id}    动物档案 + 轨迹 GeoJSON + 照片
"""
import hashlib
import json
import os
import secrets

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional

import config
from app import database
from app import sync_obis

app = FastAPI(title="Animal Bracelet")

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

PHOTOS_DIR = os.path.join(STATIC_DIR, "assets", "photos")


@app.get("/manifest.json")
def manifest():
    return FileResponse(os.path.join(STATIC_DIR, "manifest.json"), headers=_NO_CACHE_HEADERS)


@app.get("/icons/{name}")
def icons(name: str):
    return FileResponse(os.path.join(STATIC_DIR, "icons", name), headers=_NO_CACHE_HEADERS)


@app.get("/sw.js")
def sw_file():
    """Service Worker（根路径，scope=/ 全站推送）"""
    return FileResponse(os.path.join(STATIC_DIR, "sw.js"), headers=_NO_CACHE_HEADERS)


@app.get("/photos/{filename}")
def photo_file(filename: str):
    """照片文件（独立路径，绕过Service Worker对/static/的拦截）"""
    safe = os.path.basename(filename)
    path = os.path.join(PHOTOS_DIR, safe)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="照片不存在")
    return FileResponse(path, headers=_NO_CACHE_HEADERS)


def _animal_row(row):
    return {
        "id": row["id"],
        "name": row["name"],
        "species": row["species"],
        "story": row["story"],
        "origin": row["origin"],
        "data_note": row["data_note"],
        "region_label": row["region_label"] or "",
        "photos": json.loads(row["photo_urls"] or "[]"),
    }


@app.on_event("startup")
def _startup():
    database.init_db()
    if config.AUTO_SYNC and config.SYNC_SPEC:
        for animal_id, datasetid in config.SYNC_SPEC.items():
            try:
                sync_obis.sync_animal(animal_id, datasetid, pages=10)
            except Exception as e:  # 同步失败不影响启动
                print(f"[sync] {animal_id} 同步失败：{e}")


@app.post("/api/sync")
def api_sync():
    """触发一次数据同步：从 Movebank 拉取 Noé 白鹳 + Lumi 欧斑鸠最新数据。"""
    import subprocess
    import sys
    results = {}

    # 1. 从 Movebank 同步所有动物（Noé 白鹳 + Lumi 欧斑鸠）
    try:
        script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts", "sync_movebank_all.py")
        r = subprocess.run(
            [sys.executable, script_path],
            capture_output=True, text=True, timeout=300,
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        results["movebank_all"] = {
            "returncode": r.returncode,
            "stdout": r.stdout[-3000:] if len(r.stdout) > 3000 else r.stdout,
            "stderr": r.stderr[-500:] if r.stderr else ""
        }
    except Exception as e:
        results["movebank_all"] = {"error": str(e)}

    # 数据同步完成后，推送新足迹通知给已开启提醒的用户
    try:
        push_result = _push_updates_to_all()
        results["push"] = push_result
    except Exception as e:
        results["push"] = {"error": str(e)}

    return {"ok": True, "results": results}


# ---------- 页面 ----------

_NO_CACHE_HEADERS = {
    "Cache-Control": "no-cache, no-store, must-revalidate",
    "Pragma": "no-cache",
    "Expires": "0",
}


def _page(path: str):
    return FileResponse(path, headers=_NO_CACHE_HEADERS)


@app.get("/")
def index():
    return _page(os.path.join(STATIC_DIR, "index.html"))


@app.get("/c/{code}")
def claim_page(code: str):
    return _page(os.path.join(STATIC_DIR, "claim.html"))


@app.get("/animal/{animal_id}")
def animal_page(animal_id: str):
    return _page(os.path.join(STATIC_DIR, "animal.html"))


@app.get("/admin")
def admin_page(request: Request):
    """主办方管理后台（需要密码）"""
    # 会话校验：cookie 中保存的 admin_token 与 secret 派生哈希一致才放行
    token = request.cookies.get("admin_token", "")
    secret = os.environ.get("ADMIN_SECRET", "ab2026-v2-9f3c7e1a")
    expect = hashlib.sha256((secret + ":admin").encode()).hexdigest()
    if token == expect:
        return _page(os.path.join(STATIC_DIR, "admin.html"))
    # 未登录：返回一个轻量登录页（内联，避免额外文件）
    html = """<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>主办方登录 · 动物追踪手环</title><style>
body{background:#0d1b2a;color:#e0e0e0;font-family:'PingFang SC','Microsoft YaHei',sans-serif;display:flex;align-items:center;justify-content:center;min-height:100vh;margin:0}
.box{background:#132a45;border:1px solid #1f4068;border-radius:16px;padding:36px 40px;width:320px;box-shadow:0 12px 40px rgba(0,0,0,.4)}
h1{font-size:18px;margin:0 0 6px;color:#7fb2e5}
p{font-size:12.5px;color:#8aa0b8;margin:0 0 22px;line-height:1.6}
input{width:100%;box-sizing:border-box;padding:12px 14px;border-radius:10px;border:1px solid #2a4a70;background:#0d1b2a;color:#fff;font-size:15px;margin-bottom:14px;outline:none}
input:focus{border-color:#4a9eff}
button{width:100%;padding:12px;border:none;border-radius:10px;background:linear-gradient(135deg,#1a8a7d,#0f5e56);color:#fff;font-size:15px;font-weight:600;cursor:pointer}
button:hover{opacity:.9}
.err{color:#ff6b6b;font-size:12.5px;margin-top:10px;display:none}
</style></head><body>
<div class="box">
<h1>🔐 主办方管理后台</h1>
<p>只有主办方（你）能进入。请输入管理密码。</p>
<form method="post" action="/admin/login" id="f">
<input type="password" name="password" placeholder="管理密码" autofocus required>
<button type="submit">进入后台</button>
<div class="err" id="err">密码错误，请重试</div>
</form>
</div>
<script>
var hasErr = location.search.indexOf('fail=1') !== -1;
if (hasErr) { document.getElementById('err').style.display = 'block'; }
</script>
</body></html>"""
    return HTMLResponse(html, status_code=200)


@app.post("/admin/login")
def admin_login(request: Request, password: str = Form("")):
    """校验管理密码，成功则种 cookie 并跳转后台"""
    secret = os.environ.get("ADMIN_SECRET", "ab2026-v2-9f3c7e1a")
    admin_pwd = os.environ.get("ADMIN_PASSWORD", "AB2026@k8s#Xy")
    if password == admin_pwd:
        token = hashlib.sha256((secret + ":admin").encode()).hexdigest()
        resp = RedirectResponse(url="/admin", status_code=303)
        resp.set_cookie("admin_token", token, httponly=True, samesite="lax", max_age=7 * 86400)
        return resp
    return RedirectResponse(url="/admin?fail=1", status_code=303)


@app.get("/admin/logout")
def admin_logout():
    resp = RedirectResponse(url="/", status_code=303)
    resp.delete_cookie("admin_token")
    return resp


# ---------- API ----------

@app.get("/api/demo/codes")
def api_demo_codes():
    """本地演示：返回当前未使用的领养码（部署上线后建议删除或加鉴权）。"""
    conn = database.get_conn()
    rows = conn.execute(
        "SELECT code FROM claim_codes WHERE status = 'unused' ORDER BY code LIMIT 5"
    ).fetchall()
    conn.close()
    return {"codes": [r["code"] for r in rows]}


@app.get("/api/animals")
def api_animals():
    conn = database.get_conn()
    rows = conn.execute("SELECT * FROM animals ORDER BY created_at").fetchall()
    conn.close()
    return {"animals": [_animal_row(r) for r in rows]}


@app.get("/api/admin/stats")
def api_admin_stats():
    """主办方后台统计：动物数、领养码总数、已用/未用数量"""
    conn = database.get_conn()
    animal_count = conn.execute("SELECT COUNT(*) as cnt FROM animals").fetchone()["cnt"]
    total_codes = conn.execute("SELECT COUNT(*) as cnt FROM claim_codes").fetchone()["cnt"]
    used_codes = conn.execute("SELECT COUNT(*) as cnt FROM claim_codes WHERE status = 'claimed'").fetchone()["cnt"]
    unused_codes = conn.execute("SELECT COUNT(*) as cnt FROM claim_codes WHERE status = 'unused'").fetchone()["cnt"]
    # 每个动物的定位点数
    track_counts = conn.execute(
        "SELECT animal_id, COUNT(*) as cnt FROM track_points GROUP BY animal_id"
    ).fetchall()
    conn.close()
    return {
        "animal_count": animal_count,
        "total_codes": total_codes,
        "used_codes": used_codes,
        "unused_codes": unused_codes,
        "track_counts": {r["animal_id"]: r["cnt"] for r in track_counts},
    }


@app.get("/api/claim/{code}")
def api_claim_status(code: str):
    conn = database.get_conn()
    row = conn.execute(
        "SELECT c.*, a.name AS animal_name, a.species, a.story, a.photo_urls, a.id AS animal_id "
        "FROM claim_codes c JOIN animals a ON a.id = c.animal_id WHERE c.code = ?",
        (code,),
    ).fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="领养码不存在")
    animal = {
        "id": row["animal_id"],
        "name": row["animal_name"],
        "species": row["species"],
        "story": row["story"],
        "photos": json.loads(row["photo_urls"] or "[]"),
    }
    if row["status"] == "claimed":
        return {"status": "claimed", "animal": animal}
    return {"status": "unused", "animal": animal}


class ClaimRequest(BaseModel):
    nickname: Optional[str] = None


@app.post("/api/claim/{code}")
def api_claim(code: str, claim_req: ClaimRequest = None):
    nickname = claim_req.nickname if claim_req else None

    conn = database.get_conn()
    row = conn.execute("SELECT * FROM claim_codes WHERE code = ?", (code,)).fetchone()
    if row is None:
        conn.close()
        raise HTTPException(status_code=404, detail="领养码不存在")
    if row["status"] == "claimed":
        conn.close()
        raise HTTPException(status_code=409, detail="该领养码已被使用")
    conn.execute(
        "UPDATE claim_codes SET status = 'claimed', claimed_at = datetime('now'), nickname = ? WHERE code = ?",
        (nickname, code),
    )
    conn.commit()
    conn.close()
    return {"ok": True, "animal_id": row["animal_id"], "nickname": nickname}


@app.get("/api/animal/{animal_id}/latest")
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


@app.get("/api/animal/{animal_id}")
def api_animal(animal_id: str):
    conn = database.get_conn()
    row = conn.execute("SELECT * FROM animals WHERE id = ?", (animal_id,)).fetchone()
    if row is None:
        conn.close()
        raise HTTPException(status_code=404, detail="动物不存在")
    points = conn.execute(
        "SELECT ts, lat, lon, alt FROM track_points WHERE animal_id = ? ORDER BY ts", (animal_id,)
    ).fetchall()
    conn.close()

    geojson = {
        "type": "Feature",
        "properties": {"name": row["name"], "species": row["species"]},
        "geometry": {
            "type": "LineString",
            "coordinates": [[p["lon"], p["lat"], p["alt"]] for p in points],
        },
    }
    animal = _animal_row(row)
    animal["track_count"] = len(points)
    animal["track_start"] = points[0]["ts"] if points else None
    animal["track_end"] = points[-1]["ts"] if points else None
    animal["updated_at"] = points[-1]["ts"] if points else None
    return {
        "animal": animal,
        "track": geojson,
        "times": [p["ts"] for p in points],
    }


# ---------- PWA 推送 ----------

def _load_vapid():
    p = os.path.join(config.DATA_DIR, "vapid.json")
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8") as f:
        return json.load(f)


class PushSub(BaseModel):
    animal_id: str = ""
    endpoint: str
    p256dh: str = ""
    auth: str = ""


@app.get("/api/push/vapid-public-key")
def push_public_key():
    v = _load_vapid()
    if not v:
        raise HTTPException(status_code=500, detail="VAPID 未配置")
    return {"public_key": v["public_key"]}


@app.post("/api/push/subscribe")
def push_subscribe(sub: PushSub):
    conn = database.get_conn()
    conn.execute(
        "INSERT OR REPLACE INTO push_subs (animal_id, endpoint, p256dh, auth) VALUES (?,?,?,?)",
        (sub.animal_id, sub.endpoint, sub.p256dh, sub.auth),
    )
    conn.commit()
    conn.close()
    return {"ok": True}


@app.post("/api/push/unsubscribe")
def push_unsubscribe(sub: PushSub):
    if not sub.endpoint or sub.endpoint == "local":
        return {"ok": True}
    conn = database.get_conn()
    conn.execute("DELETE FROM push_subs WHERE endpoint=?", (sub.endpoint,))
    conn.commit()
    conn.close()
    return {"ok": True}


def _send_push_to_sub(sub, title, body, url):
    v = _load_vapid()
    if not v:
        return None
    try:
        from pywebpush import webpush, WebPushException
        info = {
            "endpoint": sub["endpoint"],
            "keys": {"p256dh": sub["p256dh"], "auth": sub["auth"]},
        }
        webpush(
            subscription_info=info,
            data=json.dumps({"title": title, "body": body, "url": url}, ensure_ascii=False),
            vapid_private_key=v["private_key"],
            vapid_claims={"sub": v["subject"]},
            timeout=12,
        )
        return True
    except WebPushException as e:
        if e.response is not None and e.response.status_code in (404, 410):
            return "gone"  # 订阅已失效
        return False
    except Exception:
        return False


def _push_updates_to_all():
    """数据更新后，给所有开启提醒的用户推送。"""
    try:
        conn = database.get_conn()
        subs = conn.execute("SELECT * FROM push_subs").fetchall()
        conn.close()
    except Exception:
        return {"sent": 0, "total": 0}
    sent = 0
    gone = []
    for s in subs:
        r = _send_push_to_sub(s, "🐾 它有了新足迹", "追踪数据刚刚更新，快来看看它飞到哪里了", "/")
        if r is True:
            sent += 1
        elif r == "gone":
            gone.append(s["endpoint"])
    if gone:
        try:
            conn = database.get_conn()
            for ep in gone:
                conn.execute("DELETE FROM push_subs WHERE endpoint=?", (ep,))
            conn.commit()
            conn.close()
        except Exception:
            pass
    return {"sent": sent, "total": len(subs)}


@app.post("/api/push/send")
def push_send():
    """给所有订阅者推送（数据更新后自动调用，也可手动测试）。"""
    r = _push_updates_to_all()
    return {"ok": True, **r}
