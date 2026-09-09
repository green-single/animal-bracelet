# -*- coding: utf-8 -*-
"""
全局配置
========
BASE_URL：二维码里写入的领养链接前缀。
  - 本地测试：保持 http://localhost:8000
  - 部署上线：改成你的正式域名（如 https://animal.mydomain.com），
    然后重新运行 scripts/generate_codes.py 重新生成二维码打印稿。
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "animals.db")
QRCODE_DIR = os.path.join(DATA_DIR, "qrcodes")

# 二维码中写入的地址前缀（部署后改成正式域名再重新生成二维码）
BASE_URL = os.environ.get("ANIMAL_BRACE_URL", "http://localhost:8000")

# 每只手环/每个二维码对应一只动物；生成二维码的数量
N_CODES = 20

# 服务器监听端口（Render 会自动设置 PORT 环境变量）
PORT = int(os.environ.get("PORT", "8000"))

# 自动同步配置：把哪只动物接到哪个 OBIS 真实数据集（UUID 在 obis.org 数据集页可查）
# 每只动物一个来源；运行"同步"时按此表逐条拉取更新
SYNC_SPEC = {
    # ava -> 澳大利亚东海岸绿海龟卫星追踪 2010-2011（个体 Noel）
    "ava": "6d5df2d0-f41d-4d92-87c4-8642d5a39cfa",
}

# 是否在服务启动时自动同步一次（部署到线上后建议设为 1，配合定时任务每日更新）
AUTO_SYNC = os.environ.get("ANIMAL_BRACE_AUTO_SYNC", "0") == "1"
