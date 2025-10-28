import time, pyautogui as pag
from . import __name__ as pkgname  # noqa
from ...pyauto_core import emit_log, emit_case, emit_shot, step_timer

def run(socketio, ctx):
    tenant = ctx["tenant"]
    tc = ctx.get("tc", "TC003 Test Nagative Ref2")
    emit_log(socketio, tenant, f"=== {tc} start (tenant={tenant}) ===")
    t = step_timer()

    try:
        time.sleep(10)
        pag.click(300,255)
        pag.press("enter")
        emit_log(socketio, tenant, f"ไม่คีย์ Ref2")
        time.sleep(5)
        emit_shot(socketio, tenant, "nagative", "Non_Key_Ref2")
        socketio.sleep(0)
        pag.press("enter")

        time.sleep(5)
        pag.click(300,255)
        pag.write("7")
        emit_log(socketio, tenant, f"คีย์ Ref2 < 10 หลัก")
        time.sleep(5)
        emit_shot(socketio, tenant, "nagative", "Ref2_less_than_10_digit")
        socketio.sleep(0)
        pag.press("enter")
        time.sleep(5)
        emit_shot(socketio, tenant, "nagative", "Ref2_less_than_10_digit")
        socketio.sleep(0)
        pag.press("enter")

        # time.sleep(5)
        # pag.write("123456789012345")
        # emit_log(socketio, tenant, f"คีย์ Ref2 > 10 หลัก")
        # pag.press("enter")
        # emit_shot(socketio, tenant, "nagative", "Ref2 more than 10 digit")
        # socketio.sleep(0)
        # time.sleep(5)
        # pag.press("enter")
        
        time.sleep(5)
        pag.write("700072215")
        emit_log(socketio, tenant, f"คีย์ 700072215 ที่ Ref2 สำเร็จ")
        pag.press("enter")
        
        emit_case(socketio, tenant, tc, "passed", category="Nagative Ref2", duration_sec=t.sec(), message="OK")
    except Exception as e:
        emit_shot(socketio, tenant, "nagative", f"{tc}_error")
        emit_case(socketio, tenant, tc, "failed", category="Nagative Ref2", duration_sec=t.sec(), message=str(e))
        raise
