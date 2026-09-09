# -*- coding: utf-8 -*-
"""
动物手环项目 · 文件保护与系统稳定性守护
======================================
职责（每次运行）：
  1. 完整性体检：DB非空 / 二维码65个 / 打印稿存在 / 照片在 / 代码在 / 服务运行
  2. 备份本次状态到项目外快照目录（每个快照记录各项健康标记）
  3. 异常自动恢复：从【最近一次健康快照】还原丢失/损坏的文件
  4. 服务保活：localhost:8000 未响应则重启
  5. 全部动作写日志 guard/backup.log

备份位置：C:\\DoubaoProjects\\_backups\\animal-bracelet\\snapshot_时间戳\\
保留最近 BACKUP_KEEP 份快照，自动清理更旧的。
"""
import datetime
import glob
import json
import os
import shutil
import socket
import sqlite3
import subprocess
import sys

PROJ = r"C:\DoubaoProjects\animal-bracelet"
BACKUP_ROOT = r"C:\DoubaoProjects\_backups\animal-bracelet"
LOG = os.path.join(PROJ, "guard", "backup.log")
BACKUP_KEEP = 10          # 保留快照份数
SERVICE_PORT = 8000
PYTHON = sys.executable

# 需要保护的文件/目录（相对 PROJ）
CRITICAL = [
    "data/animals.db",
    "data/animals_seed.json",
    "data/qrcodes",          # 整个目录：65个二维码PNG + codes.json + 清单
    "data/print_sheets",
    "app/static/assets/photos",
    "app/main.py",
    "app/database.py",
    "app/static/index.html",
    "app/static/animal.html",
    "app/static/claim.html",
    "app/static/admin.html",
    "config.py",
    "run.py",
    "scripts/sync_movebank_all.py",
    ".github/workflows/sync-db.yml",
    "guard/guard.ps1",
]
MIN_DB_ROWS = 6          # animals 表至少 6 只
MIN_QR_CODES = 65        # 二维码至少 65 个


def log(msg):
    line = f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} {msg}"
    print(line)
    try:
        os.makedirs(os.path.dirname(LOG), exist_ok=True)
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


# ---------- 健康检查 ----------
def db_ok():
    p = os.path.join(PROJ, "data", "animals.db")
    if not os.path.exists(p) or os.path.getsize(p) < 1024:
        return False
    try:
        c = sqlite3.connect(p)
        n = c.execute("SELECT COUNT(*) FROM animals").fetchone()[0]
        c.close()
        return n >= MIN_DB_ROWS
    except Exception:
        return False


def qr_ok():
    p = os.path.join(PROJ, "data", "qrcodes")
    if not os.path.isdir(p):
        return False
    return len(glob.glob(os.path.join(p, "*.png"))) >= MIN_QR_CODES


def sheet_ok():
    p = os.path.join(PROJ, "data", "print_sheets")
    return os.path.isdir(p) and bool(glob.glob(os.path.join(p, "*.pdf"))) and \
        len(glob.glob(os.path.join(p, "sheet_*.png"))) >= 7


def photos_ok():
    p = os.path.join(PROJ, "app", "static", "assets", "photos")
    return os.path.isdir(p) and len(glob.glob(os.path.join(p, "*.jpg"))) >= 24


def service_ok():
    """重试3次避免瞬时抖动误报"""
    for _ in range(3):
        try:
            s = socket.create_connection(("127.0.0.1", SERVICE_PORT), timeout=2)
            s.close()
            return True
        except Exception:
            import time
            time.sleep(3)
    return False


# ---------- 备份 ----------
def do_backup(flags):
    """复制关键文件到快照目录，记录健康标记"""
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    snap = os.path.join(BACKUP_ROOT, "snapshot_" + ts)
    os.makedirs(snap, exist_ok=True)
    copied = 0
    for rel in CRITICAL:
        src = os.path.join(PROJ, rel)
        if not os.path.exists(src):
            continue
        dst = os.path.join(snap, rel)
        try:
            if os.path.isdir(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)
            copied += 1
        except Exception as e:
            log(f"[backup] 失败: {rel} -> {e}")
    with open(os.path.join(snap, "_snapshot.json"), "w", encoding="utf-8") as f:
        json.dump({"time": ts, "copied": copied, "healthy": flags}, f, ensure_ascii=False)
    log(f"[backup] 快照 {ts} ({copied}项, 健康项: " +
        ", ".join(k for k, v in flags.items() if v) + ")")
    cleanup_old()
    return snap


def cleanup_old():
    snaps = sorted(glob.glob(os.path.join(BACKUP_ROOT, "snapshot_*")))
    while len(snaps) > BACKUP_KEEP:
        old = snaps.pop(0)
        try:
            shutil.rmtree(old, ignore_errors=True)
            log(f"[backup] 清理旧快照 {old}")
        except Exception:
            pass


def snapshot_flags(snap):
    p = os.path.join(snap, "_snapshot.json")
    if not os.path.exists(p):
        return {}
    try:
        return json.load(open(p, encoding="utf-8")).get("healthy") or {}
    except Exception:
        return {}


def restore_from(rel, snap):
    """从指定快照恢复单个路径"""
    src = os.path.join(snap, rel)
    if not os.path.exists(src):
        log(f"[restore] 快照 {os.path.basename(snap)} 无 {rel}")
        return False
    dst = os.path.join(PROJ, rel)
    try:
        if os.path.isdir(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
        log(f"[restore] ✅ 已从快照 {os.path.basename(snap)} 恢复 {rel}")
        return True
    except Exception as e:
        log(f"[restore] 恢复失败 {rel}: {e}")
        return False


def restore_best(rel, key):
    """从最近一份该 key 为健康(true)的快照恢复"""
    snaps = sorted(glob.glob(os.path.join(BACKUP_ROOT, "snapshot_*")))
    for snap in reversed(snaps):
        flags = snapshot_flags(snap)
        if flags.get(key) is True:
            if restore_from(rel, snap):
                return True
    log(f"[restore] 无健康快照可恢复 {rel} (key={key})")
    return False


# ---------- 主流程 ----------
def run_checks():
    # 1. 体检（不恢复）
    checks = {
        "db": db_ok,
        "qr": qr_ok,
        "sheet": sheet_ok,
        "photos": photos_ok,
    }
    flags = {k: fn() for k, fn in checks.items()}
    missing = [rel for rel in CRITICAL if not os.path.exists(os.path.join(PROJ, rel))]
    problems = [k for k, v in flags.items() if not v] + \
               [f"缺失:{rel}" for rel in missing]

    # 2. 备份本次状态（含健康标记）
    do_backup(flags)

    # 3. 异常恢复（从最近健康快照）
    if not flags["db"]:
        log("[check] ⚠️ 数据库异常")
        if not restore_best("data/animals.db", "db") and not db_ok():
            # 兜底：删坏库，让服务重启从种子自动导入
            try:
                os.remove(os.path.join(PROJ, "data", "animals.db"))
                log("[db] 无健康备份, 删除坏库交由种子自愈")
            except Exception:
                pass
    if not flags["qr"]:
        log("[check] ⚠️ 二维码异常")
        restore_best("data/qrcodes", "qr")
    if not flags["sheet"]:
        log("[check] ⚠️ 打印稿异常")
        restore_best("data/print_sheets", "sheet")
    if not flags["photos"]:
        log("[check] ⚠️ 照片异常")
        restore_best("app/static/assets/photos", "photos")
    for rel in missing:
        restore_best(rel, "db" if "db" in rel else "qr")

    # 4. 服务保活
    if not service_ok():
        log("[service] 服务未运行, 正在重启")
        try:
            subprocess.Popen([PYTHON, "run.py"], cwd=PROJ,
                             creationflags=subprocess.CREATE_NO_WINDOW)
        except Exception as e:
            log(f"[service] 启动失败: {e}")
        import time
        time.sleep(5)

    # 5. 复检
    again = {k: fn() for k, fn in checks.items()}
    ok_now = all(again.values()) and service_ok()
    if ok_now and not problems:
        log("[check] ✅ 全部正常 (DB/二维码/打印稿/照片/代码/服务)")
    else:
        remain = [k for k, v in again.items() if not v]
        log(f"[check] ⚠️ 复检仍有问题: {remain or '服务未响应'} (原问题: {problems})")


if __name__ == "__main__":
    run_checks()
