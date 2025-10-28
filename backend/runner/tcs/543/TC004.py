import time, pyautogui as pag
from . import __name__ as pkgname  # noqa
from ...pyauto_core import emit_log, emit_case, emit_shot, step_timer

def run(socketio, ctx):
    tenant = ctx["tenant"]
    tc = ctx.get("tc", "TC004 Test Nagative Amount")
    emit_log(socketio, tenant, f"=== {tc} start (tenant={tenant}) ===")
    t = step_timer()

    try:
        time.sleep(15)
        pag.click(437, 645)
        emit_log(socketio, tenant, f"คลิกปุ่ม แก้ไข สำเร็จ")

        time.sleep(5)
        pag.press("backspace")
        pag.press("enter")
        emit_log(socketio, tenant, f"ไม่คีย์จำนวนเงิน")
        time.sleep(5)
        emit_shot(socketio, tenant, "nagative", "Non_key_Amount")
        socketio.sleep(0)
        pag.press("enter")

        time.sleep(5)
        pag.click(399,563)
        time.sleep(0.5)
        pag.write('0')
        pag.press("enter")
        emit_log(socketio, tenant, f"คีย์จำนวนเงินน้อยกว่าที่รับชำระ")
        emit_shot(socketio, tenant, "nagative", "Amount_Min")
        socketio.sleep(0)
        pag.press("enter")
        time.sleep(5)
        emit_shot(socketio, tenant, "nagative", "Amount_Min")

        time.sleep(5)
        pag.click(399,563)
        time.sleep(0.5)
        pag.write('30001' , interval=0.2)
        pag.press("enter")
        emit_log(socketio, tenant, f"คีย์จำนวนเงินมากกว่าที่รับชำระ")
        emit_shot(socketio, tenant, "nagative", "Amount_Max")
        socketio.sleep(0)
        pag.press("enter")
        time.sleep(5)
        emit_shot(socketio, tenant, "nagative", "Amount_Max")
        time.sleep(2)
        pag.press("esc")
        
        emit_case(socketio, tenant, tc, "passed", category="Nagative Amount", duration_sec=t.sec(), message="OK")
    except Exception as e:
        emit_shot(socketio, tenant, "nagative", f"{tc}_error")
        emit_case(socketio, tenant, tc, "failed", category="Nagative Amount", duration_sec=t.sec(), message=str(e))
        raise
