import importlib
import importlib.util
import os
import time
from .pyauto_core import emit_log

ALL_TCS = ["TC001" , "TC002" , "TC003"]  # เพิ่มตามจริง เช่น ["TC001","TC002","TC003",...]
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def _load_from_path(py_path: str):
    """Fallback: โหลดไฟล์ .py จาก path โดยตรง แล้วดึงฟังก์ชัน run"""
    if not os.path.isfile(py_path):
        raise ModuleNotFoundError(py_path)
    mod_name = f"_tc_dynamic_{hash(py_path)}"
    spec = importlib.util.spec_from_file_location(mod_name, py_path)
    m = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(m)  # type: ignore[attr-defined]
    if not hasattr(m, "run"):
        raise AttributeError(f"{py_path} does not define run(socketio, ctx)")
    return m.run

def _load_tc(tenant: str, tc: str):
    tc_upper = tc
    tc_lower = tc.lower()

    candidates = [
        f"runner.tcs.{tenant}.{tc_upper}",
        f"runner.tcs.{tenant}.{tc_lower}",
    ]
    for mod in candidates:
        try:
            run_fn = importlib.import_module(mod).run  # type: ignore[attr-defined]
            return run_fn
        except ModuleNotFoundError:
            pass
        except AttributeError:
            # โมดูลมี แต่ไม่มีฟังก์ชัน run
            raise

    # หาไฟล์ตาม path ตรง
    by_path = [
        os.path.join(BASE_DIR, "backend", "runner", "tcs", tenant, f"{tc_upper}.py"),
        os.path.join(BASE_DIR, "backend", "runner", "tcs", tenant, f"{tc_lower}.py"),
    ]
    for p in by_path:
        try:
            return _load_from_path(p)
        except ModuleNotFoundError:
            continue
    raise ModuleNotFoundError(f"No testcase module for {tc} (tenant={tenant})")

def run_suite(socketio, tenant_code: str, selected=None):
    emit_log(socketio, tenant_code, f"เริ่มรันชุดทดสอบสำหรับผู้ว่าจ้าง {tenant_code}")
    start = time.perf_counter()

    tcs = selected or ALL_TCS
    total = len(tcs); passed = 0; failed = 0

    for tc in tcs:
        try:
            run_fn = _load_tc(tenant_code, tc)
            run_fn(socketio, {"tenant": tenant_code, "tc": tc})
            passed += 1
        except Exception as e:
            failed += 1
            emit_log(socketio, tenant_code, f"[{tc}] ERROR: {e}")

    dur = round(time.perf_counter() - start, 2)
    socketio.emit("test_case_summary", {"total": total, "passed": passed, "failed": failed, "duration_sec": dur})
    emit_log(socketio, tenant_code, f"สรุป: total={total}, passed={passed}, failed={failed}, duration={dur}s")