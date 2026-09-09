# -*- coding: utf-8 -*-
import os

def dirsize(p):
    total = 0
    for root, dirs, files in os.walk(p):
        for f in files:
            try:
                total += os.path.getsize(os.path.join(root, f))
            except Exception:
                pass
    return total

def fmt(n):
    for u in ['B', 'KB', 'MB', 'GB']:
        if n < 1024:
            return '%.1f%s' % (n, u)
        n /= 1024
    return '%.1fTB' % n

print('=== C:\\DoubaoProjects 相关目录占用 ===')
total = 0
rows = []
for t in ['animal-bracelet', '_backups', '_git_backup_animal']:
    p = os.path.join('C:\\DoubaoProjects', t)
    if os.path.exists(p):
        s = dirsize(p)
        total += s
        rows.append((t, s))

for t, s in rows:
    print('%-32s %10s' % (t, fmt(s)))
print('-' * 46)
print('%-32s %10s' % ('合计', fmt(total)))

print()
print('=== 项目内部分类占用 (animal-bracelet) ===')
proj = 'C:\\DoubaoProjects\\animal-bracelet'
for sub in ['data', 'app', 'scripts', 'guard', '.git', 'photos_orig']:
    p = os.path.join(proj, sub)
    if os.path.exists(p):
        print('%-32s %10s' % (sub + '/', fmt(dirsize(p))))

# 项目根下散落的大文件
print()
print('=== 项目根目录大文件(>1MB) ===')
for f in os.listdir(proj):
    p = os.path.join(proj, f)
    if os.path.isfile(p):
        s = os.path.getsize(p)
        if s > 1024 * 1024:
            print('%-32s %10s' % (f, fmt(s)))
