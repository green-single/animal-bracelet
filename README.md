# 动物追踪手环 · DIY 项目

扫码领养一只真实迁徙的动物：手环吊牌上的二维码 → 手机扫码 → 领养 → 回放迁徙轨迹、浏览照片。

**当前状态**：系统已完整跑通，内置 5 只示例动物（轨迹为模拟数据，用于演示）。接入 Movebank 真实数据的方法见下文。

---

## 一、目录结构

```
animal-bracelet/
├── run.py                      # 启动入口：python run.py
├── config.py                   # 配置：BASE_URL / 码数量 / 端口
├── requirements.txt            # 依赖
├── app/
│   ├── main.py                 # FastAPI 后端（领养校验、动物、轨迹接口）
│   ├── database.py             # SQLite 数据库
│   ├── seed.py                 # 5 只示例动物 + 模拟轨迹
│   └── static/                 # 前端页面（首页 / 领养页 / 动物主页）
│       └── assets/             # 本地照片 + Leaflet 地图库（离线自足）
├── scripts/
│   ├── generate_codes.py       # 批量生成领养码 + 二维码 PNG
│   ├── make_print_sheet.py     # A4 打印拼版（PNG）
│   ├── import_movebank_csv.py  # 从 Movebank CSV 导入真实轨迹
│   └── reset_codes.py          # 重置全部领养码为未使用（开发用）
└── data/
    ├── animals.db              # SQLite 数据库
    ├── qrcodes/                # 20 个二维码 PNG + codes.json 清单
    └── print_sheets/           # A4 打印稿（sheet_1/2.png + PDF）
```

## 二、快速开始（本地跑通）

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 初始化示例数据（5 只动物，300 个轨迹点）
python -m app.seed

# 3. 生成 20 个领养码 + 二维码（已生成过可跳过）
python scripts/generate_codes.py

# 4. 启动服务
python run.py
```

打开浏览器访问 `http://localhost:8000`，首页有「模拟扫码」区，输入领养码即可体验完整流程：
**输入码 → 领养页 → 确认领养 → 动物主页（轨迹回放 + 照片）**。

## 三、做手环（打印 → 组装）

1. 打印 `data/print_sheets/二维码打印稿_A4.pdf`（2 页，每页 10 个码，300dpi）
2. 按十字裁切线裁剪，每个二维码约 3.5cm，可贴到吊牌/卡片上
3. 买编织/硅胶手环（1688/淘宝，1~5 元/条），把吊牌穿上去
4. 朋友拿到手环 → 手机相机扫二维码 → 领养 → 看轨迹

> 二维码内容 = `http://localhost:8000/c/领养码`。**本地测试用这个地址**；
> 部署上线后（见下）需要重新生成一次二维码（改 BASE_URL 后重跑 generate_codes.py）。

## 四、部署上线（免费 + 数据自动更新）

**已内置：真实数据自动同步（OBIS）+ 免费部署方案。**

1. 看 **[DEPLOY.md](DEPLOY.md)**：GitHub + Render 免费层 + GitHub Actions 定时同步 = 0 成本、数据时时流动
2. 手机在任何地方扫码可用（二维码要指向正式域名）
3. 上线后改 `config.py` 的 `BASE_URL`，**重新运行**：
   ```bash
   python scripts/generate_codes.py
   ```
4. 重新生成打印稿：`python scripts/make_print_sheet.py`
5. 重新打印，此时二维码指向正式域名，手机在任何地方扫码都能用

> 部署注意：SQLite 适合个人 demo；用户量大了可换 PostgreSQL（代码逻辑不变，只改数据库层）。
> 免费层实例重启不保留磁盘 → 已支持 `ANIMAL_BRACE_AUTO_SYNC=1` 启动自动从 OBIS 重建数据。

## 五、真实动物数据（核心升级 · 已可用）

系统现在能**直接接入真实遥测数据并持续更新**，两种方式：

- **OBIS（海洋动物，无需注册，推荐）**：见 `scripts/fetch_real_data.py` 和 `app/sync_obis.py`；
  示例：`python scripts/fetch_real_data.py --datasetid <UUID> --id ava --limit 300`
- **Movebank（陆地/鸟类，需注册）**：下载 CSV 后运行 `python scripts/import_movebank_csv.py --csv 你的研究.csv --id maya --name Maya --species "绿海龟" --limit 300`

> 数据许可：Movebank / OBIS 各数据集许可不同（CC0 / CC BY / CC BY-NC 等），
> 个人 demo 与学术用途（SURF 等）没问题；商用前务必核对数据集许可条款并署名。

## 六、常见问题

**地图瓦片不显示？**
已内置 3 个瓦片源自动切换：OSM → Esri 卫星图 → Carto，网络不通时自动换源。
若都不通（完全离线环境），轨迹线和数据仍正常，仅底图为空白。

**照片为什么是这几张？**
示例数据使用 Wikimedia Commons 的 CC 协议动物照片，已下载到本地 `app/static/assets/photos/`，
页面会标注作者与许可。接入真实数据后，可在数据库中更新 `photo_urls` 换成你自己的照片。

**想要 NFC 版（手机碰一碰）？**
买 NTAG215 贴片（阿里巴巴约 0.5~2 元/个），用手机 NFC 工具把
`http://你的域名/c/领养码` 写入贴片，贴在吊牌内侧，手机一碰即打开领养页。
二维码与 NFC 可并存（码相同）。

**领养码用完了/想换一批？**
```bash
python scripts/reset_codes.py   # 全部重置为未使用
python scripts/generate_codes.py # 或生成更多新码
```

## 七、接口速查

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/` | 首页（demo 入口） |
| GET | `/c/{code}` | 扫码领养页 |
| GET | `/animal/{id}` | 动物主页（地图 + 照片） |
| GET | `/api/animals` | 动物列表 |
| GET | `/api/claim/{code}` | 查询领养码状态 |
| POST | `/api/claim/{code}` | 执行领养（一码一次） |
| GET | `/api/animal/{id}` | 动物档案 + 轨迹 GeoJSON |
| GET | `/api/demo/codes` | 未使用领养码（本地演示用） |

## 2026-09-05 进展记录
- 新增第 6 只动物 **Nuri**（宁加卢绿海龟）：真实遥测，来源 CSIRO/BHP「Ningaloo Outlook」项目（OBIS 公开数据），追踪期 2023-12-19 至 2024-04-19（筑巢季），166 个真实检测点。
- 数据源验证：**Happywhale 照片识别数据库**（OBIS 镜像，CC0 许可）含座头鲸个体档案（如 Kaos），目击记录至 2025-07，个体有真实照片（happywhale.com/individual/6313）。已下载 Kaos 真实个体照片至 app/static/assets/photos/kaos_1.jpg；完整目击轨迹待网络稳定后从 OBIS 全量拉取接入。
- 首页优化：动物卡片新增「真实追踪」徽章（origin=obis 显示），文案更新为真实数据说明。
