import os
import shutil
from flask import Flask, jsonify, send_from_directory
from flask_socketio import SocketIO
from data import cards
from runner.run_suite import run_suite

app = Flask(__name__, static_folder=None)
try:
    import gevent
    ASYNC_MODE = "gevent"
except Exception:
    ASYNC_MODE = "threading"
socketio = SocketIO(app, cors_allowed_origins="*", async_mode=ASYNC_MODE)

SCREENSHOT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "screenshots"))
LOG_ROOT        = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs"))

@app.get("/api/cards")
def api_cards():
    return jsonify(cards)

@app.route("/static/<tenant>/<category>/<filename>")
def serve_screenshot(tenant, category, filename):
    if category not in ("result", "nagative"):
        return "Invalid category", 404
    folder = os.path.join(SCREENSHOT_ROOT, tenant, category)
    return send_from_directory(folder, filename)

def _clear_tenant_artifacts(tenant: str):
    # ลบ screenshots/<tenant>/* และ logs/<tenant>/*
    s_dir = os.path.join(SCREENSHOT_ROOT, tenant)
    l_dir = os.path.join(LOG_ROOT, tenant)
    for d in (s_dir, l_dir):
        if os.path.isdir(d):
            shutil.rmtree(d, ignore_errors=True)
    # สร้างโฟลเดอร์พื้นฐานใหม่
    os.makedirs(os.path.join(s_dir, "result"), exist_ok=True)
    os.makedirs(os.path.join(s_dir, "nagative"), exist_ok=True)
    os.makedirs(l_dir, exist_ok=True)

@socketio.on("start_test")
def on_start_test(payload):
    # payload: {"code": "084", "tcs": ["TC001","TC006"]}  หรือ {"code":"084"} เพื่อรันทั้งหมด
    code = payload["code"] if isinstance(payload, dict) else payload
    tcs = payload.get("tcs") if isinstance(payload, dict) else None
    
    _clear_tenant_artifacts(code)

    socketio.start_background_task(run_suite, socketio, code, tcs)

if __name__ == "__main__":
    kwargs = {}
    if ASYNC_MODE == "threading":
        kwargs["allow_unsafe_werkzeug"] = True
    socketio.run(app, host="0.0.0.0", port=5000, **kwargs)
