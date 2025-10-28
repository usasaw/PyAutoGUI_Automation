import time, pyautogui as pag
from . import __name__ as pkgname  # noqa
from ...pyauto_core import emit_log, emit_case, emit_shot, step_timer

def run(socketio, ctx):
    tenant = ctx["tenant"]
    tc = ctx.get("tc", "TC002 Tax ID + Service")
    emit_log(socketio, tenant, f"=== {tc} start (tenant={tenant}) ===")
    t = step_timer()

    try:
        time.sleep(2)
        pag.click(754, 137)
        emit_log(socketio, tenant, f"คลิกปุ่ม กรอกบาร์โค้ด")

        time.sleep(5)
        pag.click(416, 386)
        time.sleep(0.5)
        pag.write("010554611368401" , interval=0.2)
        emit_log(socketio, tenant, f"คีย์ 010554611368401 ที่ Barcode สำเร็จ")
        emit_shot(socketio, tenant, "result", "Barcode_TaxID_SV")
        socketio.sleep(0)
        
        time.sleep(2)
        pag.click(487, 463)

        time.sleep(10)
        emit_log(socketio, tenant, f"รอกดปุ่มที่ EDC")
        time.sleep(5)
        emit_shot(socketio, tenant, "result", "wait_EDC")
        socketio.sleep(0)

        time.sleep(10)
        pag.click(664, 529)
        emit_log(socketio, tenant, f"คลิกปุ่ม ข้ามเสียบบัตร สำเร็จ")
        emit_shot(socketio, tenant, "result", "Skip_ID_Card")
        socketio.sleep(0)

        time.sleep(10)
        emit_shot(socketio, tenant, "result", "Detail_page_TaxID_SV")
        socketio.sleep(0)

        time.sleep(2)
        pag.press("esc")

        emit_case(socketio, tenant, tc, "passed", category="Success", duration_sec=t.sec(), message="OK")
    except Exception as e:
        emit_shot(socketio, tenant, "nagative", f"{tc}_error")
        emit_case(socketio, tenant, tc, "failed", category="Success", duration_sec=t.sec(), message=str(e))
        raise
