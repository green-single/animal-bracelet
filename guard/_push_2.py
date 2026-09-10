# -*- coding: utf-8 -*-
"""PWA推送落地(2/3)：main.py 推送端点 + sync后自动推送"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
P = 'app/main.py'
c = open(P, encoding='utf-8', newline='').read()
crlf = '\r\n' in c
c = c.replace('\r\n', '\n')

# ---------- 追加推送代码到文件末尾 ----------
PUSH_CODE = '''

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
'''

# ---------- sync 成功后自动推送 ----------
old_sync_tail = '    return {"ok": True, "results": results}'
new_sync_tail = '''    # 数据同步完成后，推送新足迹通知给已开启提醒的用户
    try:
        push_result = _push_updates_to_all()
        results["push"] = push_result
    except Exception as e:
        results["push"] = {"error": str(e)}

    return {"ok": True, "results": results}'''

assert old_sync_tail in c, 'sync尾部未找到'
c = c.replace(old_sync_tail, new_sync_tail, 1)
c = c.rstrip() + '\n' + PUSH_CODE

open(P, 'w', encoding='utf-8', newline='\n').write(c)
print('main.py 推送端点已加 | 原CRLF:', crlf, '→ LF')
print('push端点数:', c.count('/api/push'))
print('sync推送钩子:', c.count('_push_updates_to_all()'))
