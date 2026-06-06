"""数据库连接与初始化"""
import sqlite3
import os
from datetime import date
import config


def get_connection():
    """获取数据库连接"""
    if config.DB_MODE == "mysql":
        import mysql.connector
        return mysql.connector.connect(**config.MYSQL_CONFIG)
    else:
        conn = sqlite3.connect(config.SQLITE_PATH)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        return conn


def init_db():
    """初始化数据库表结构和种子数据"""
    if config.DB_MODE == "mysql":
        _init_mysql()
    else:
        _init_sqlite()


def _init_sqlite():
    conn = sqlite3.connect(config.SQLITE_PATH)
    conn.execute("PRAGMA foreign_keys=ON")
    cur = conn.cursor()

    cur.executescript("""
    CREATE TABLE IF NOT EXISTS baselines (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        domain TEXT NOT NULL DEFAULT '',
        phase TEXT NOT NULL DEFAULT '',
        ecu_count INTEGER DEFAULT 0,
        creator TEXT DEFAULT '',
        created_date TEXT,
        frozen_date TEXT,
        status TEXT DEFAULT '开发中',
        description TEXT DEFAULT ''
    );

    CREATE TABLE IF NOT EXISTS versions (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        project TEXT DEFAULT '',
        domain TEXT DEFAULT '',
        ecu TEXT DEFAULT '',
        major INTEGER DEFAULT 0,
        minor INTEGER DEFAULT 0,
        patch INTEGER DEFAULT 0,
        phase TEXT DEFAULT '',
        rxswin TEXT DEFAULT '',
        status TEXT DEFAULT '开发中',
        baseline_id TEXT,
        created_date TEXT,
        FOREIGN KEY (baseline_id) REFERENCES baselines(id) ON DELETE SET NULL
    );

    CREATE TABLE IF NOT EXISTS config_items (
        id TEXT PRIMARY KEY,
        type TEXT NOT NULL DEFAULT '',
        name TEXT NOT NULL DEFAULT '',
        version TEXT DEFAULT '',
        location TEXT DEFAULT '',
        baseline_id TEXT NOT NULL,
        FOREIGN KEY (baseline_id) REFERENCES baselines(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS changes (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL DEFAULT '',
        type TEXT DEFAULT 'ECR',
        urgency TEXT DEFAULT '普通',
        status TEXT DEFAULT '待评审',
        applicant TEXT DEFAULT '',
        baseline_id TEXT,
        created_date TEXT,
        FOREIGN KEY (baseline_id) REFERENCES baselines(id) ON DELETE SET NULL
    );

    CREATE TABLE IF NOT EXISTS releases (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL DEFAULT '',
        type TEXT DEFAULT '',
        ecu_count INTEGER DEFAULT 0,
        version TEXT DEFAULT '',
        status TEXT DEFAULT '',
        created_date TEXT
    );

    CREATE TABLE IF NOT EXISTS release_baselines (
        release_id TEXT NOT NULL,
        baseline_id TEXT NOT NULL,
        PRIMARY KEY (release_id, baseline_id),
        FOREIGN KEY (release_id) REFERENCES releases(id) ON DELETE CASCADE,
        FOREIGN KEY (baseline_id) REFERENCES baselines(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL DEFAULT '',
        size TEXT DEFAULT '',
        type TEXT DEFAULT '',
        baseline_id TEXT NOT NULL,
        file_path TEXT DEFAULT '',
        uploaded_date TEXT,
        FOREIGN KEY (baseline_id) REFERENCES baselines(id) ON DELETE CASCADE
    );
    """)

    # 插入种子数据（仅在空表时）
    cur.execute("SELECT COUNT(*) FROM baselines")
    if cur.fetchone()[0] == 0:
        _seed_data(cur)

    conn.commit()
    conn.close()


def _init_mysql():
    import mysql.connector
    # 先创建数据库
    cfg = {k: v for k, v in config.MYSQL_CONFIG.items() if k != "database"}
    cfg.pop("database", None)
    try:
        conn = mysql.connector.connect(**cfg)
        cur = conn.cursor()
        cur.execute(f"CREATE DATABASE IF NOT EXISTS {config.MYSQL_CONFIG['database']} "
                     "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        conn.close()
    except mysql.connector.Error:
        pass

    conn = mysql.connector.connect(**config.MYSQL_CONFIG)
    cur = conn.cursor()

    # 读取并执行 schema.sql
    schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema.sql")
    with open(schema_path, "r", encoding="utf-8") as f:
        sql = f.read()
    for stmt in sql.split(";"):
        stmt = stmt.strip()
        if stmt and not stmt.startswith("--"):
            try:
                # 替换 USE vsms 和 CREATE DATABASE（已处理）
                if stmt.upper().startswith("USE ") or stmt.upper().startswith("CREATE DATABASE"):
                    continue
                cur.execute(stmt)
            except mysql.connector.Error as e:
                if "Duplicate" not in str(e) and "already exists" not in str(e):
                    print(f"  [WARN] {e}")

    conn.commit()
    conn.close()


def _seed_data(cur):
    today = date.today().isoformat()

    cur.executemany(
        "INSERT INTO baselines (id, name, domain, phase, ecu_count, creator, created_date, frozen_date, status, description) VALUES (?,?,?,?,?,?,?,?,?,?)",
        [
            ("BL-001", "A_Vehicle_Baseline_DV_20260415", "整车", "DV", 86, "骞剑策", "2026-04-01", "2026-04-15", "已冻结", "全车DV阶段基线"),
            ("BL-002", "A_Vehicle_ADAS_V3.2.0_Baseline", "智驾", "PV", 12, "张工", "2026-04-25", None, "评审中", "智驾域PV阶段基线"),
            ("BL-003", "A_Vehicle_Body_V1.5.0_Baseline", "车身", "DV", 28, "骞剑策", "2026-04-10", "2026-04-20", "已冻结", "车身域DV基线"),
            ("BL-004", "A_Vehicle_Powertrain_V2.1.0", "三电", "A样", 15, "李工", "2026-03-15", "2026-04-01", "已冻结", "三电域A样基线"),
            ("BL-005", "A_Vehicle_Cockpit_V4.5.0_Baseline", "座舱", "PV", 22, "王工", "2026-05-01", None, "开发中", "座舱域PV基线"),
        ])

    cur.executemany(
        "INSERT INTO versions (id, name, project, domain, ecu, major, minor, patch, phase, rxswin, status, baseline_id, created_date) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
        [
            ("V-001", "A_Vehicle_ADAS_ADAS_DCU_3.2.1_PV", "A_Vehicle", "智驾", "ADAS_DCU", 3, 2, 1, "PV", "RXS-A_Vehicle-ADAS-001", "测试中", "BL-002", "2026-04-01"),
            ("V-002", "A_Vehicle_Body_BCM_2.3.1_PV", "A_Vehicle", "车身", "BCM", 2, 3, 1, "PV", "RXS-A_Vehicle-BCM-001", "已冻结", "BL-003", "2026-04-10"),
            ("V-003", "A_Vehicle_ADAS_Radar_Front_2.1.0_DV", "A_Vehicle", "智驾", "Radar_Front", 2, 1, 0, "DV", "RXS-A_Vehicle-RDR-001", "已冻结", "BL-001", "2026-03-20"),
            ("V-004", "A_Vehicle_Cockpit_IVI_HU_4.5.2_PV", "A_Vehicle", "座舱", "IVI_HU", 4, 5, 2, "PV", "RXS-A_Vehicle-IVI-001", "开发中", "BL-005", "2026-04-20"),
            ("V-005", "A_Vehicle_Powertrain_VCU_5.1.3_PV", "A_Vehicle", "三电", "VCU", 5, 1, 3, "PV", "RXS-A_Vehicle-VCU-001", "测试中", "BL-004", "2026-04-05"),
            ("V-006", "A_Vehicle_Body_Cluster_3.0.1_DV", "A_Vehicle", "座舱", "Cluster", 3, 0, 1, "DV", "RXS-A_Vehicle-CLS-001", "已冻结", "BL-003", "2026-03-28"),
            ("V-007", "A_Vehicle_Powertrain_BMS_2.3.0_DV", "A_Vehicle", "三电", "BMS", 2, 3, 0, "DV", "RXS-A_Vehicle-BMS-001", "已冻结", "BL-001", "2026-03-15"),
            ("V-008", "A_Vehicle_Chassis_EPS_1.8.2_A", "A_Vehicle", "底盘", "EPS", 1, 8, 2, "A样", "RXS-A_Vehicle-EPS-001", "开发中", None, "2026-04-01"),
            ("V-009", "A_Vehicle_ADAS_Camera_Main_2.5.0_DV", "A_Vehicle", "智驾", "Camera_Main", 2, 5, 0, "DV", "RXS-A_Vehicle-CAM-001", "已冻结", "BL-001", "2026-03-10"),
            ("V-010", "A_Vehicle_Cockpit_HUD_1.2.0_A", "A_Vehicle", "座舱", "HUD", 1, 2, 0, "A样", "RXS-A_Vehicle-HUD-001", "开发中", None, "2026-04-15"),
        ])

    cur.executemany(
        "INSERT INTO config_items (id, type, name, version, location, baseline_id) VALUES (?,?,?,?,?,?)",
        [
            ("CI-001", "源码", "ADAS_Application", "3.2.1", "Git: adas/app", "BL-002"),
            ("CI-002", "二进制", "ADAS_DCU_Firmware", "3.2.1", "Artifactory: /firmware", "BL-002"),
            ("CI-003", "标定", "Radar_Calibration", "2.1.0", "Artifactory: /calib", "BL-001"),
            ("CI-004", "文档", "ADAS_Release_Note", "3.2.1", "Confluence: /docs", "BL-002"),
            ("CI-005", "源码", "BCM_Application", "2.3.1", "Git: body/bcm", "BL-003"),
            ("CI-006", "二进制", "VCU_Firmware", "5.1.3", "Artifactory: /firmware", "BL-004"),
            ("CI-007", "标定", "BMS_Calibration", "2.3.0", "Artifactory: /calib", "BL-001"),
        ])

    cur.executemany(
        "INSERT INTO changes (id, title, type, urgency, status, applicant, baseline_id, created_date) VALUES (?,?,?,?,?,?,?,?)",
        [
            ("ECR-2026-0501", "OTA签名算法升级", "ECR", "紧急", "待评审", "王工", None, "2026-05-01"),
            ("ECR-2026-0429", "EPS标定数据更新", "ECR", "普通", "待评审", "赵工", None, "2026-04-29"),
            ("ECR-2026-0428", "BCM休眠逻辑参数", "ECR", "普通", "待评审", "李工", "BL-003", "2026-04-28"),
            ("ECR-2026-0425", "通信矩阵接口变更", "ECR", "紧急", "评审中", "张工", "BL-002", "2026-04-25"),
            ("ECR-2026-0420", "VCU诊断协议变更", "ECR", "普通", "实施中", "刘工", "BL-004", "2026-04-20"),
            ("ECR-2026-0418", "标定参数适配", "ECR", "普通", "实施中", "周工", None, "2026-04-18"),
            ("ECR-2026-0415", "CAN网络唤醒源变更", "ECR", "普通", "已关闭", "孙工", "BL-001", "2026-04-15"),
        ])

    cur.executemany(
        "INSERT INTO releases (id, name, type, ecu_count, version, status, created_date) VALUES (?,?,?,?,?,?,?)",
        [
            ("REL-001", "A_Vehicle_OTA_20260430", "OTA", 8, "3.2.1", "准出通过", "2026-04-30"),
            ("REL-002", "A_Vehicle_DV_Baseline_Package", "基线", 86, "1.0.0", "准出通过", "2026-04-15"),
            ("REL-003", "A_Vehicle_ADAS_Hotfix_20260420", "Hotfix", 3, "3.2.1-hotfix1", "准出通过", "2026-04-20"),
        ])

    cur.executemany(
        "INSERT INTO release_baselines (release_id, baseline_id) VALUES (?,?)",
        [
            ("REL-001", "BL-002"), ("REL-001", "BL-003"),
            ("REL-002", "BL-001"), ("REL-002", "BL-003"), ("REL-002", "BL-004"),
            ("REL-003", "BL-002"),
        ])

    cur.executemany(
        "INSERT INTO files (name, size, type, baseline_id, file_path, uploaded_date) VALUES (?,?,?,?,?,?)",
        [
            ("ADAS_v3.2.1_ReleaseNote.pdf", "2.4 MB", "文档", "BL-002", "", "2026-04-28"),
            ("BCM_Calibration_v2.3.1.bin", "156 KB", "标定", "BL-003", "", "2026-04-20"),
            ("A_Vehicle_CAN_Matrix_v4.0.xlsx", "890 KB", "文档", "BL-001", "", "2026-04-10"),
        ])
