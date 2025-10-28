import os, io, time, logging, base64
import pyautogui as pag
from datetime import datetime

pag.FAILSAFE = True
pag.PAUSE = 0.1

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SHOT_ROOT = os.path.join(ROOT_DIR, "screenshots")
LOG_ROOT  = os.path.join(ROOT_DIR, "logs")

MAX_INLINE_BYTES = 800_000

def _tenant_dirs(tenant: str):
    tshot = os.path.join(SHOT_ROOT, tenant)
    tlog  = os.path.join(LOG_ROOT, tenant)
    os.makedirs(os.path.join(tshot, "result"), exist_ok=True)
    os.makedirs(os.path.join(tshot, "nagative"), exist_ok=True)
    os.makedirs(tlog, exist_ok=True)
    return tshot, tlog

def make_logger(tenant: str):
    _tenant_dirs(tenant)
    logger = logging.getLogger(f"AUTORUN_{tenant}")
    # ป้องกันซ้ำ handler
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    fh = logging.FileHandler(os.path.join(LOG_ROOT, tenant, "automation.log"), encoding="utf-8")
    fh.setFormatter(fmt); logger.addHandler(fh)
    sh = logging.StreamHandler()
    sh.setFormatter(fmt); logger.addHandler(sh)
    return logger

def screenshot(tenant: str, category="result", prefix="step"):
    tshot, _ = _tenant_dirs(tenant)
    cat = category if category in ("result", "nagative") else "result"
    ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    fname = f"{ts}_{prefix}.png"
    folder = os.path.join(tshot, cat)
    path = os.path.join(folder, fname)

    pag.screenshot(path , region=(6,86,798,596) )
    size = os.path.getsize(path)
    b64 = None
    if size <= MAX_INLINE_BYTES:
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
    return path, b64, fname, cat

def emit_log(socketio, tenant: str, msg: str):
    make_logger(tenant).info(msg)
    socketio.emit("test_result", msg)

def emit_case(socketio, tenant: str, name: str, status: str, category: str = "", duration_sec: float = 0, message: str = ""):
    payload = {"name": name, "status": status, "category": category, "duration_sec": duration_sec, "message": message}
    socketio.emit("test_case_result", payload)
    make_logger(tenant).info(f"[{name}] {status} ({duration_sec}s) {message}")

def emit_shot(socketio, tenant: str, category="result", prefix="step"):
    try:
        path, b64, fname, cat = screenshot(tenant, category, prefix)
        payload = {
            "filename": fname,
            "url": f"/static/{tenant}/{cat}/{fname}",
            "category": cat,
        }
        if b64 is not None:
            payload["base64"] = b64
        socketio.emit("screenshot", payload)
        # ให้โอกาส async switch
        try: 
            socketio.sleep(0)
        except Exception: 
            pass
        return path
    except Exception as e:
        socketio.emit("test_result", f"[emit_shot] ERROR: {e}")
        try: 
            socketio.sleep(0)
        except Exception: 
            pass
        return None
    
class step_timer:
    def __init__(self): self._t = time.perf_counter()
    def sec(self): return round(time.perf_counter() - self._t, 2)