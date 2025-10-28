import time, pyautogui as pag
from . import __name__ as pkgname  # noqa
from ...pyauto_core import emit_log, emit_case, emit_shot, step_timer

def run(socketio, ctx):
    tenant = ctx["tenant"]
    tc = ctx.get("tc", "TC002 Test Nagative Ref1")
    emit_log(socketio, tenant, f"=== {tc} start (tenant={tenant}) ===")
    t = step_timer()

    try:
        pag.click(55, 260)
        emit_log(socketio, tenant, f"คลิก Counter Service")

        time.sleep(10)
        pag.click(340, 215)
        emit_log(socketio, tenant, f"คลิกกลุ่มทรู")

        time.sleep(10)
        emit_log(socketio, tenant, f"รอกดปุ่มที่ EDC")

        time.sleep(10)
        pag.click(664, 529)
        emit_log(socketio, tenant, f"คลิกปุ่ม ข้ามเสียบบัตร สำเร็จ")

        time.sleep(10)
        pag.press("enter")
        emit_log(socketio, tenant, f"ไม่คีย์ Ref1")
        time.sleep(5)
        emit_shot(socketio, tenant, "nagative", "Non_Key_Ref1")
        socketio.sleep(0)
        pag.press("enter")

        time.sleep(5)
        pag.click(297,215)
        pag.write("7")
        emit_log(socketio, tenant, f"คีย์ Ref1 < 10 หลัก")
        time.sleep(5)
        emit_shot(socketio, tenant, "nagative", "Ref1_less_than_10_digit")
        socketio.sleep(0)
        pag.press("enter")
        time.sleep(5)
        emit_shot(socketio, tenant, "nagative", "Ref1_less_than_10_digit")
        socketio.sleep(0)
        pag.press("enter")
        
        # time.sleep(5)
        # pag.write("123456789012345")
        # emit_log(socketio, tenant, f"คีย์ Ref1 > 10 หลัก")
        # pag.press("enter")
        # emit_shot(socketio, tenant, "nagative", "Ref1 more than 10 digit")
        # socketio.sleep(0)
        # time.sleep(5)
        # pag.press("enter")
        
        time.sleep(5)
        pag.write("700072215")
        emit_log(socketio, tenant, f"คีย์ 700072215 ที่ Ref1 สำเร็จ")
        pag.press("enter")
        
        emit_case(socketio, tenant, tc, "passed", category="Nagative Ref1", duration_sec=t.sec(), message="OK")
    except Exception as e:
        emit_shot(socketio, tenant, "nagative", f"{tc}_error")
        emit_case(socketio, tenant, tc, "failed", category="Nagative Ref1", duration_sec=t.sec(), message=str(e))
        raise
