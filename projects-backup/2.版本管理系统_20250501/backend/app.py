"""版本管理系统 Flask REST API"""
import os
import uuid
import json
from datetime import date
from flask import Flask, request, jsonify, send_from_directory
import config
from db import get_connection, init_db

app = Flask(__name__, static_folder="../", static_url_path="")


# ========== 工具函数 ==========

def row_to_dict(row):
    """将数据库行转为字典"""
    if row is None:
        return None
    if isinstance(row, dict):
        return row
    return dict(row)


def rows_to_list(rows):
    return [row_to_dict(r) for r in rows]


def json_serial(obj):
    """JSON 序列化处理 date 类型"""
    if isinstance(obj, (date,)):
        return obj.isoformat()


# ========== 首页 ==========

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "version-management-system.html")


# ========== 基线 API ==========

@app.route("/api/baselines", methods=["GET"])
def list_baselines():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM baselines ORDER BY created_date DESC")
    rows = cur.fetchall()
    conn.close()
    return jsonify(rows_to_list(rows))


@app.route("/api/baselines/<id>", methods=["GET"])
def get_baseline(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM baselines WHERE id=?", (id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "Not found"}), 404
    return jsonify(row_to_dict(row))


@app.route("/api/baselines", methods=["POST"])
def create_baseline():
    data = request.json
    conn = get_connection()
    cur = conn.cursor()
    # 生成 ID
    if not data.get("id"):
        cur.execute("SELECT COUNT(*) FROM baselines")
        n = cur.fetchone()[0] + 1
        data["id"] = f"BL-{n:03d}"
    cur.execute(
        "INSERT INTO baselines (id, name, domain, phase, ecu_count, creator, created_date, frozen_date, status, description) "
        "VALUES (?,?,?,?,?,?,?,?,?,?)",
        (data["id"], data.get("name", ""), data.get("domain", ""), data.get("phase", ""),
         data.get("ecuCount", data.get("ecu_count", 0)), data.get("creator", ""),
         data.get("createdDate", data.get("created_date", date.today().isoformat())),
         data.get("frozenDate", data.get("frozen_date", None)),
         data.get("status", "开发中"), data.get("description", ""))
    )
    conn.commit()
    conn.close()
    return jsonify(data), 201


@app.route("/api/baselines/<id>", methods=["PUT"])
def update_baseline(id):
    data = request.json
    conn = get_connection()
    cur = conn.cursor()
    fields = []
    values = []
    for key in ["name", "domain", "phase", "ecu_count", "creator", "frozen_date", "status", "description"]:
        if key in data:
            fields.append(f"{key}=?")
            values.append(data[key])
    if "ecuCount" in data:
        fields.append("ecu_count=?")
        values.append(data["ecuCount"])
    if "createdDate" in data:
        fields.append("created_date=?")
        values.append(data["createdDate"])
    if "frozenDate" in data:
        fields.append("frozen_date=?")
        values.append(data["frozenDate"])
    if not fields:
        return jsonify({"error": "No fields to update"}), 400
    values.append(id)
    cur.execute(f"UPDATE baselines SET {', '.join(fields)} WHERE id=?", values)
    conn.commit()
    conn.close()
    return jsonify({"ok": True})


@app.route("/api/baselines/<id>", methods=["DELETE"])
def delete_baseline(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM baselines WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"ok": True})


# ========== 版本 API ==========

@app.route("/api/versions", methods=["GET"])
def list_versions():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM versions ORDER BY created_date DESC")
    rows = cur.fetchall()
    conn.close()
    return jsonify(rows_to_list(rows))


@app.route("/api/versions", methods=["POST"])
def create_version():
    data = request.json
    conn = get_connection()
    cur = conn.cursor()
    if not data.get("id"):
        cur.execute("SELECT COUNT(*) FROM versions")
        n = cur.fetchone()[0] + 1
        data["id"] = f"V-{n:03d}"
    cur.execute(
        "INSERT INTO versions (id, name, project, domain, ecu, major, minor, patch, phase, rxswin, status, baseline_id, created_date) "
        "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (data["id"], data.get("name", ""), data.get("project", ""), data.get("domain", ""),
         data.get("ecu", ""), data.get("major", 0), data.get("minor", 0), data.get("patch", 0),
         data.get("phase", ""), data.get("rxswin", ""), data.get("status", "开发中"),
         data.get("baselineId", data.get("baseline_id", None)),
         data.get("createdDate", data.get("created_date", date.today().isoformat())))
    )
    conn.commit()
    conn.close()
    return jsonify(data), 201


@app.route("/api/versions/<id>", methods=["PUT"])
def update_version(id):
    data = request.json
    conn = get_connection()
    cur = conn.cursor()
    fields = []
    values = []
    for key in ["name", "project", "domain", "ecu", "major", "minor", "patch", "phase", "rxswin", "status", "baseline_id"]:
        if key in data:
            fields.append(f"{key}=?")
            values.append(data[key])
    if "baselineId" in data:
        fields.append("baseline_id=?")
        values.append(data["baselineId"])
    if "createdDate" in data:
        fields.append("created_date=?")
        values.append(data["createdDate"])
    if not fields:
        return jsonify({"error": "No fields to update"}), 400
    values.append(id)
    cur.execute(f"UPDATE versions SET {', '.join(fields)} WHERE id=?", values)
    conn.commit()
    conn.close()
    return jsonify({"ok": True})


@app.route("/api/versions/<id>", methods=["DELETE"])
def delete_version(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM versions WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"ok": True})


# ========== 配置项 API ==========

@app.route("/api/config-items", methods=["GET"])
def list_config_items():
    baseline_id = request.args.get("baseline_id")
    conn = get_connection()
    cur = conn.cursor()
    if baseline_id:
        cur.execute("SELECT * FROM config_items WHERE baseline_id=? ORDER BY id", (baseline_id,))
    else:
        cur.execute("SELECT * FROM config_items ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return jsonify(rows_to_list(rows))


@app.route("/api/config-items", methods=["POST"])
def create_config_item():
    data = request.json
    conn = get_connection()
    cur = conn.cursor()
    if not data.get("id"):
        cur.execute("SELECT COUNT(*) FROM config_items")
        n = cur.fetchone()[0] + 1
        data["id"] = f"CI-{n:03d}"
    cur.execute(
        "INSERT INTO config_items (id, type, name, version, location, baseline_id) VALUES (?,?,?,?,?,?)",
        (data["id"], data.get("type", ""), data.get("name", ""), data.get("version", ""),
         data.get("location", ""), data.get("baselineId", data.get("baseline_id", "")))
    )
    conn.commit()
    conn.close()
    return jsonify(data), 201


@app.route("/api/config-items/<id>", methods=["PUT"])
def update_config_item(id):
    data = request.json
    conn = get_connection()
    cur = conn.cursor()
    fields = []
    values = []
    for key in ["type", "name", "version", "location"]:
        if key in data:
            fields.append(f"{key}=?")
            values.append(data[key])
    if "baselineId" in data:
        fields.append("baseline_id=?")
        values.append(data["baselineId"])
    elif "baseline_id" in data:
        fields.append("baseline_id=?")
        values.append(data["baseline_id"])
    if not fields:
        return jsonify({"error": "No fields to update"}), 400
    values.append(id)
    cur.execute(f"UPDATE config_items SET {', '.join(fields)} WHERE id=?", values)
    conn.commit()
    conn.close()
    return jsonify({"ok": True})


@app.route("/api/config-items/<id>", methods=["DELETE"])
def delete_config_item(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM config_items WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"ok": True})


# ========== 变更 API ==========

@app.route("/api/changes", methods=["GET"])
def list_changes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM changes ORDER BY created_date DESC")
    rows = cur.fetchall()
    conn.close()
    return jsonify(rows_to_list(rows))


@app.route("/api/changes", methods=["POST"])
def create_change():
    data = request.json
    conn = get_connection()
    cur = conn.cursor()
    if not data.get("id"):
        cur.execute("SELECT COUNT(*) FROM changes")
        n = cur.fetchone()[0] + 1
        data["id"] = f"ECR-{date.today().strftime('%Y')}-{n:04d}"
    cur.execute(
        "INSERT INTO changes (id, title, type, urgency, status, applicant, baseline_id, created_date) VALUES (?,?,?,?,?,?,?,?)",
        (data["id"], data.get("title", ""), data.get("type", "ECR"), data.get("urgency", "普通"),
         data.get("status", "待评审"), data.get("applicant", ""),
         data.get("baselineId", data.get("baseline_id", None)),
         data.get("createdDate", data.get("created_date", date.today().isoformat())))
    )
    conn.commit()
    conn.close()
    return jsonify(data), 201


@app.route("/api/changes/<id>", methods=["PUT"])
def update_change(id):
    data = request.json
    conn = get_connection()
    cur = conn.cursor()
    fields = []
    values = []
    for key in ["title", "type", "urgency", "status", "applicant", "baseline_id"]:
        if key in data:
            fields.append(f"{key}=?")
            values.append(data[key])
    if "baselineId" in data:
        fields.append("baseline_id=?")
        values.append(data["baselineId"])
    if not fields:
        return jsonify({"error": "No fields to update"}), 400
    values.append(id)
    cur.execute(f"UPDATE changes SET {', '.join(fields)} WHERE id=?", values)
    conn.commit()
    conn.close()
    return jsonify({"ok": True})


@app.route("/api/changes/<id>", methods=["DELETE"])
def delete_change(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM changes WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"ok": True})


# ========== 发布 API ==========

@app.route("/api/releases", methods=["GET"])
def list_releases():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM releases ORDER BY created_date DESC")
    releases = rows_to_list(cur.fetchall())
    for rel in releases:
        cur.execute("SELECT baseline_id FROM release_baselines WHERE release_id=?", (rel["id"],))
        rel["baseline_ids"] = [r[0] if isinstance(r, tuple) else r["baseline_id"] for r in cur.fetchall()]
    conn.close()
    return jsonify(releases)


@app.route("/api/releases", methods=["POST"])
def create_release():
    data = request.json
    conn = get_connection()
    cur = conn.cursor()
    if not data.get("id"):
        cur.execute("SELECT COUNT(*) FROM releases")
        n = cur.fetchone()[0] + 1
        data["id"] = f"REL-{n:03d}"
    cur.execute(
        "INSERT INTO releases (id, name, type, ecu_count, version, status, created_date) VALUES (?,?,?,?,?,?,?)",
        (data["id"], data.get("name", ""), data.get("type", ""),
         data.get("ecuCount", data.get("ecu_count", 0)), data.get("version", ""),
         data.get("status", ""), data.get("createdDate", data.get("created_date", date.today().isoformat())))
    )
    # 关联基线
    baseline_ids = data.get("baselineIds", data.get("baseline_ids", []))
    for bid in baseline_ids:
        cur.execute("INSERT OR IGNORE INTO release_baselines (release_id, baseline_id) VALUES (?,?)",
                     (data["id"], bid))
    conn.commit()
    conn.close()
    return jsonify(data), 201


@app.route("/api/releases/<id>", methods=["PUT"])
def update_release(id):
    data = request.json
    conn = get_connection()
    cur = conn.cursor()
    fields = []
    values = []
    for key in ["name", "type", "ecu_count", "version", "status"]:
        if key in data:
            fields.append(f"{key}=?")
            values.append(data[key])
    if "ecuCount" in data:
        fields.append("ecu_count=?")
        values.append(data["ecuCount"])
    if not fields:
        return jsonify({"error": "No fields to update"}), 400
    values.append(id)
    cur.execute(f"UPDATE releases SET {', '.join(fields)} WHERE id=?", values)
    # 更新基线关联
    if "baselineIds" in data or "baseline_ids" in data:
        baseline_ids = data.get("baselineIds", data.get("baseline_ids", []))
        cur.execute("DELETE FROM release_baselines WHERE release_id=?", (id,))
        for bid in baseline_ids:
            cur.execute("INSERT OR IGNORE INTO release_baselines (release_id, baseline_id) VALUES (?,?)", (id, bid))
    conn.commit()
    conn.close()
    return jsonify({"ok": True})


@app.route("/api/releases/<id>", methods=["DELETE"])
def delete_release(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM releases WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"ok": True})


# ========== 文件 API ==========

@app.route("/api/files", methods=["GET"])
def list_files():
    baseline_id = request.args.get("baseline_id")
    conn = get_connection()
    cur = conn.cursor()
    if baseline_id:
        cur.execute("SELECT * FROM files WHERE baseline_id=? ORDER BY uploaded_date DESC", (baseline_id,))
    else:
        cur.execute("SELECT * FROM files ORDER BY uploaded_date DESC")
    rows = cur.fetchall()
    conn.close()
    return jsonify(rows_to_list(rows))


@app.route("/api/files/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    f = request.files["file"]
    baseline_id = request.form.get("baseline_id") or request.form.get("baselineId")
    if not baseline_id:
        return jsonify({"error": "baseline_id is required"}), 400

    # 保存文件
    ext = os.path.splitext(f.filename)[1] if f.filename else ""
    saved_name = f"{uuid.uuid4().hex}{ext}"
    saved_path = os.path.join(config.UPLOAD_DIR, saved_name)
    f.save(saved_path)

    # 文件大小
    size_bytes = os.path.getsize(saved_path)
    if size_bytes < 1024:
        size_str = f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        size_str = f"{size_bytes / 1024:.1f} KB"
    else:
        size_str = f"{size_bytes / (1024 * 1024):.1f} MB"

    # 推断类型
    ext_lower = ext.lower()
    type_map = {".pdf": "文档", ".doc": "文档", ".docx": "文档", ".xls": "文档", ".xlsx": "文档",
                ".bin": "标定", ".hex": "标定", ".s19": "标定",
                ".c": "源码", ".cpp": "源码", ".h": "源码", ".py": "源码",
                ".zip": "压缩包", ".tar": "压缩包", ".gz": "压缩包"}
    file_type = request.form.get("type") or type_map.get(ext_lower, "其他")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO files (name, size, type, baseline_id, file_path, uploaded_date) VALUES (?,?,?,?,?,?)",
        (f.filename, size_str, file_type, baseline_id, saved_name, date.today().isoformat())
    )
    file_id = cur.lastrowid
    conn.commit()
    conn.close()

    return jsonify({
        "id": file_id,
        "name": f.filename,
        "size": size_str,
        "type": file_type,
        "baseline_id": baseline_id,
        "file_path": saved_name,
        "uploaded_date": date.today().isoformat()
    }), 201


@app.route("/api/files/<int:id>/download", methods=["GET"])
def download_file(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM files WHERE id=?", (id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "Not found"}), 404
    row = row_to_dict(row)
    return send_from_directory(config.UPLOAD_DIR, row["file_path"], download_name=row["name"])


@app.route("/api/files/<int:id>", methods=["DELETE"])
def delete_file(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT file_path FROM files WHERE id=?", (id,))
    row = cur.fetchone()
    if row:
        file_path = row[0] if isinstance(row, tuple) else row["file_path"]
        full_path = os.path.join(config.UPLOAD_DIR, file_path)
        if os.path.exists(full_path):
            os.remove(full_path)
        cur.execute("DELETE FROM files WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"ok": True})


# ========== 统计 API ==========

@app.route("/api/stats", methods=["GET"])
def get_stats():
    conn = get_connection()
    cur = conn.cursor()
    stats = {}
    for table in ["baselines", "versions", "config_items", "changes", "releases", "files"]:
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        stats[table] = cur.fetchone()[0]
    conn.close()
    return jsonify(stats)


# ========== 启动 ==========

if __name__ == "__main__":
    print("初始化数据库...")
    init_db()
    print("启动 Flask 服务: http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
