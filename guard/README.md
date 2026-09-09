# 文件保护与系统稳定性守护

项目运行期间自动保护所有关键文件，防止数据丢失/损坏/服务宕机。

## 保护范围（自动备份到项目外）

| 内容 | 路径 | 说明 |
|---|---|---|
| 数据库 | data/animals.db | 12只动物+65领养码+9088定位点 |
| 种子文件 | data/animals_seed.json | 数据库的JSON备份（自动恢复用） |
| 二维码 | data/qrcodes/ | 65个PNG + codes.json + 清单 |
| 打印稿 | data/print_sheets/ | A4打印PDF + 7页PNG |
| 照片 | app/static/assets/photos/ | 全部动物照片 |
| 代码 | app/*.py + app/static/*.html 等 | 核心代码 |

**备份位置**：`C:\DoubaoProjects\_backups\animal-bracelet\snapshot_时间戳\`
**保留策略**：最近 10 份快照，旧的自动清理。

## 三层保护机制

```
第1层 服务保活 guard.ps1       每30秒检查 localhost:8000，挂了自动重启
第2层 文件守护 backup.py       每2小时：体检+备份+异常自动从健康快照恢复
第3层 种子自愈 database.py     数据库丢失时，服务启动自动从seed.json重建
```

## 每2小时自动运行（Windows计划任务）

任务名：`AB_FileGuard_Hourly`
- 运行内容：`guard/run_backup.vbs`（隐藏窗口，不打扰）
- 调用：`guard/backup.py`

**手动运行一次**：
```
schtasks /Run /TN AB_FileGuard_Hourly
```
或直接：`python C:\DoubaoProjects\animal-bracelet\guard\backup.py`

## 守护日志

- 备份/恢复记录：`guard/backup.log`
- 服务保活记录：`guard/guard.log`

## 恢复能力（已实测）

| 丢失内容 | 恢复方式 | 结果 |
|---|---|---|
| animals.db | 从健康快照恢复；快照也坏→种子自愈 | ✅ 12只动物 |
| 二维码PNG | 从健康快照恢复 | ✅ 65个 |
| 打印稿PDF | 从健康快照恢复 | ✅ 7页 |
| 照片 | 从健康快照恢复 | ✅ 全部 |
| 服务宕机 | guard.ps1 自动重启 | ✅ |

## 注意

- 备份目录在项目外（`C:\DoubaoProjects\_backups\`），项目内文件全删也能恢复
- 计划任务以当前用户运行，电脑开机后需登录一次才生效；如长时间不登录，可用任何登录后首次运行兜底（下次手动运行一次即可）
- GitHub远程仓库也保存了代码+数据+种子（网络可用时自动同步）
