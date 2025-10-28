import time
from .pyauto_core import emit_log

from .tcs.tc001_success import run as run_tc001
# from .tcs.tc002_xxx import run as run_tc002  # เพิ่มตามจริง

SUITE_MAP = {
    "TC001": run_tc001,
    # "TC002": run_tc002,
}

def run_suite(socketio, tenant_code, selected=None):
    """
    selected: list of test IDs (เช่น ["TC001","TC002"]) ถ้า None = รันทั้งหมด
    """
    emit_log(socketio, f"เริ่มรันชุดทดสอบสำหรับผู้ว่าจ้าง {tenant_code}")
    start = time.perf_counter()

    tcs = selected or list(SUITE_MAP.keys())
    total = len(tcs)
    passed = 0; failed = 0

    for tc in tcs:
        try:
            SUITE_MAP[tc](socketio, {"tenant": tenant_code, "params": {}})
            passed += 1
        except Exception:
            failed += 1

    dur = round(time.perf_counter() - start, 2)
    socketio.emit("test_case_summary", {"total": total, "passed": passed, "failed": failed, "duration_sec": dur})
    emit_log(socketio, f"สรุป: total={total}, passed={passed}, failed={failed}, duration={dur}s")
