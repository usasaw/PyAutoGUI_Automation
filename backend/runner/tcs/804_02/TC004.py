import time, pyautogui as pag
from . import __name__ as pkgname
from ...pyauto_core import emit_log, emit_case, emit_shot, step_timer

def run(socketio, ctx):
    tenant = ctx["tenant"]
    tc = ctx.get("tc", "TC004 One Touch ช่องทางที่ 1 : หน้าหลัก")
    # tc = ctx.get("tc", "TC005 One Touch ช่องทางที่ 2 : กลุ่มผู้ว่าจ้าง >>>  ซื้อ/ชำระค่าตั๋ว All Ticket >>> ซื้อตั๋วเครื่องบิน")
    # tc = ctx.get("tc", "TC006 Reprint")
    # tc = ctx.get("tc", "TC007 Fullform")
    # tc = ctx.get("tc", "TC008 OR")
    # tc = ctx.get("tc", "TC009 ไม่คีย Ref 1 - Booking No.")
    # tc = ctx.get("tc", "TC010 Ref 1 < 12 หลัก")
    # tc = ctx.get("tc", "TC011 Ref 1 > 17 หลัก 17501+Booking No.")
    emit_log(socketio, tenant, f"=== {tc} start (tenant={tenant}) ===")
    t = step_timer()

    try:
        time.sleep(2)
        pag.click(59, 265)
        emit_log(socketio, tenant, f"คลิกปุ่ม Counter Service")

        time.sleep(5)
        pag.click(465, 207)
        emit_log(socketio, tenant, f"คลิกปุ่ม ไทยแอร์เอเชีย สำเร็จ")

        time.sleep(5)
        emit_shot(socketio, tenant, "result", f"Click_Service_01")
        socketio.sleep(0)
        time.sleep(1)
        pag.click(417, 295)
        emit_log(socketio, tenant, f"เลือก Service 01 สำเร็จ")

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
        pag.click(297,215)
        pag.write('17501120234041213', interval=0.2)
        time.sleep(0.5)
        emit_shot(socketio, tenant, "result", "คีย์ Ref1")
        socketio.sleep(0)
        pag.press('enter')

    except Exception as e:
        emit_shot(socketio, tenant, "nagative", f"{tc}_error")
        emit_case(socketio, tenant, tc, "faild", category="Nagative Search", duration_sec=t.sec(), message=str(e))
        raise