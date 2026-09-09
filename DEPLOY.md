# 免费永久部署 + 数据自动更新指南

## 目标

- **免费**：整个系统 0 成本运行（代码托管、服务运行、数据源全部免费）。
- **可长期**：没有单点付费依赖；即使服务偶尔休眠也能自动恢复。
- **数据时时流动**：轨迹不是固定老数据，系统定时从 OBIS（公开海洋生物数据库）拉取最新真实遥测记录，自动合并更新。

## 成本与免费层级说明（先看这个）

| 组成 | 用什么 | 费用 | 说明 |
|---|---|---|---|
| 代码托管 | GitHub 私有仓库 | 免费 | 永久 |
| 网站运行 | Render 免费层（Web Service） | 免费 | 750 小时/月足够个人/小规模；15 分钟无人访问会休眠，首次访问唤醒约 30~60 秒；免费层实例重启后磁盘不保留 → 数据靠"启动自动同步"重建 |
| 数据源 | OBIS 公开数据库 | 免费 | 无需注册，API 直接拉取（CC 协议数据） |
| 定时更新 | GitHub Actions（schedule cron） | 免费 | 每天自动调一次同步接口，与网站休眠无关 |
| 二维码 | 本机脚本生成 | 免费 | 打印只需 A4 纸 |

> 诚实提示：互联网不存在"永久免费"的绝对承诺，任何平台都可能调整政策。
> 这套组合的容错在于——**代码和数据都在你手里**（GitHub + 本地），
> 换平台重新部署只需 10 分钟。

## 第一步：部署到 Render（免费）

1. 把项目推到 GitHub：
   ```bash
   cd C:\DoubaoProjects\animal-bracelet
   git init && git add . && git commit -m "animal bracelet"
   # 在 github.com 新建私有仓库后：
   git remote add origin https://github.com/<你的用户名>/animal-bracelet.git
   git push -u origin main
   ```

2. 打开 https://render.com → 注册 → **New → Web Service** → 连接你的仓库。

3. 关键配置：
   - **Build Command**：`pip install -r requirements.txt`
   - **Start Command**：`python run.py`（服务监听 0.0.0.0:8000，Render 会自动映射）
   - **Environment Variables**：
     - `ANIMAL_BRACE_URL` = `https://你的应用名.onrender.com`（部署完成后回填）
     - `ANIMAL_BRACE_AUTO_SYNC` = `1`（启动时自动从 OBIS 同步，解决免费层磁盘不持久的问题）

4. 部署完成后，把 `ANIMAL_BRACE_URL` 改成正式地址，然后**重新生成二维码**：
   ```bash
   python scripts/generate_codes.py
   python scripts/make_print_sheet.py
   ```
   新打印稿在 `data/print_sheets/`。

## 第二步：数据自动更新（时时流动）

系统现在自带：
- `POST /api/sync` —— 从 OBIS 拉取最新记录合并进轨迹（增量、去重）
- 启动自动同步（`ANIMAL_BRACE_AUTO_SYNC=1`）

### 每天定时更新（GitHub Actions，免费）

在仓库创建 `.github/workflows/sync.yml`：

```yaml
name: sync
on:
  schedule:
    - cron: "0 2 * * *"   # 每天 UTC 02:00（北京 10:00）
  workflow_dispatch:
jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - run: curl -s -X POST https://你的应用名.onrender.com/api/sync
```

这样每天自动拉一次真实数据，轨迹始终"活着"。

### 同步哪些动物

`config.py` 里的 `SYNC_SPEC` 决定每只动物接哪个 OBIS 数据集：

```python
SYNC_SPEC = {
    "ava": "6d5df2d0-f41d-4d92-87c4-8642d5a39cfa",  # 澳大利亚绿海龟 Noel（真实）
    # "koa": "换成另一个 OBIS 数据集 UUID",
}
```

在 https://obis.org 搜索物种 → 打开数据集页 → 复制 UUID 填进去，重启后即接入新数据源。
支持任意多种动物，每只一个来源。

### 其他真实数据源

- **Movebank**（陆地/鸟类追踪）：注册免费账号 → Tracking Data Map → 接受许可下载 CSV → `python scripts/import_movebank_csv.py --csv xxx.csv --id koa`
- **OBIS 手动全量**：`python scripts/fetch_real_data.py --datasetid <UUID> --id <动物id> --limit 300`

## 第三步：域名（可选）

- 免费：Render 自带 `*.onrender.com` 子域名，够用。
- 想要更好看的域名：买一个便宜域名（约 ¥30/年），在 Render 控制台绑定并配 HTTPS。
- **绑定后务必重新生成二维码**，否则扫码仍指向旧地址。

## 上线检查清单

- [ ] 手机浏览器打开正式域名，首页正常
- [ ] 用手机扫新生成的二维码 → 领养页 → 确认领养 → 地图/轨迹/照片正常
- [ ] 同一码扫第二次 → "已有主人"提示
- [ ] 手动触发一次 `POST /api/sync`，确认返回 `added/total`
- [ ] 换域名前已重新生成二维码并打印
