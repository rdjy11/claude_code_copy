"""数据库配置"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 数据库模式: 'sqlite' 或 'mysql'
DB_MODE = os.environ.get("VSMS_DB_MODE", "sqlite")

# SQLite 配置
SQLITE_PATH = os.path.join(BASE_DIR, "vsms.db")

# MySQL 配置（DB_MODE=mysql 时生效）
MYSQL_CONFIG = {
    "host": os.environ.get("VSMS_MYSQL_HOST", "localhost"),
    "port": int(os.environ.get("VSMS_MYSQL_PORT", "3306")),
    "user": os.environ.get("VSMS_MYSQL_USER", "root"),
    "password": os.environ.get("VSMS_MYSQL_PASSWORD", ""),
    "database": os.environ.get("VSMS_MYSQL_DB", "vsms"),
    "charset": "utf8mb4",
}

UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
