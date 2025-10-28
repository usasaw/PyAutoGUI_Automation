import time, pyautogui as pag
from . import __name__ as pkgname  # noqa
from ...pyauto_core import emit_log, emit_case, emit_shot, step_timer

def run(socketio, ctx):
    tenant = ctx["tenant"]
    tc = ctx.get("tc", "TC001 Success")
    emit_log(socketio, tenant, f"=== {tc} start (tenant={tenant}) ===")
    t = step_timer()

    try:
        pag.click(55, 260)
        emit_log(socketio, tenant, f"คลิก Counter Service")
        emit_shot(socketio, tenant, "result", "Counter_Service")
        socketio.sleep(0)

        time.sleep(10)
        pag.click(340, 215)
        emit_log(socketio, tenant, f"คลิกกลุ่มทรู")
        emit_shot(socketio, tenant, "result", "Click_True")
        socketio.sleep(0)

        time.sleep(10)
        emit_log(socketio, tenant, f"รอกดปุ่มที่ EDC")
        emit_shot(socketio, tenant, "result", "wait_EDC")
        socketio.sleep(0)

        time.sleep(10)
        pag.click(664, 529)
        emit_log(socketio, tenant, f"คลิกปุ่ม ข้ามเสียบบัตร สำเร็จ")
        emit_shot(socketio, tenant, "result", "Skip_ID_Card")
        socketio.sleep(0)

        time.sleep(10)
        pag.write("700072215")
        emit_log(socketio, tenant, f"คีย์ 700072215 ที่ Ref1 สำเร็จ")
        emit_shot(socketio, tenant, "result", "Key_Ref1")
        socketio.sleep(0)
        pag.press("enter")

        time.sleep(2)
        pag.write("700072215")
        emit_log(socketio, tenant, f"คีย์ 700072215 ที่ Ref2 สำเร็จ")
        emit_shot(socketio, tenant, "result", "Key_Ref2")
        socketio.sleep(0)
        pag.press("enter")

        time.sleep(15)
        pag.click(437, 645)
        emit_log(socketio, tenant, f"คลิกปุ่ม แก้ไข สำเร็จ")
        emit_shot(socketio, tenant, "result", "Click_Edit_Amount")
        socketio.sleep(0)

        time.sleep(3)
        pag.write("100")
        emit_log(socketio, tenant, f"คีย์ จำนวนเงิน 100 บาท สำเร็จ")
        emit_shot(socketio, tenant, "result", "Edit_Amount")
        socketio.sleep(0)

        time.sleep(5)
        pag.click(665, 640)
        emit_log(socketio, tenant, f"คลิกปุ่ม ยืนยันการทำรายการ สำเร็จ")
        emit_shot(socketio, tenant, "result", "Confirm_transaction")
        socketio.sleep(0)

        time.sleep(5)
        pag.click(774, 640)
        emit_log(socketio, tenant, f"คลิกปุ่ม ยืนยัน สำเร็จ")
        emit_shot(socketio, tenant, "result", "Confirm_to_pay")
        socketio.sleep(0)

        time.sleep(10)
        pag.click(566, 640)
        emit_log(socketio, tenant, f"คลิกปุ่ม ชำระเงิน สำเร็จ")
        emit_shot(socketio, tenant, "result", "Payment")
        socketio.sleep(0)

        time.sleep(5)
        pag.click(566, 634)
        emit_log(socketio, tenant, f"คลิกปุ่ม รับพอดี สำเร็จ")

        time.sleep(5)
        pag.click(486, 430)
        emit_log(socketio, tenant, f"คลิกปุ่ม ยืนยัน สำเร็จ")
        
        emit_case(socketio, tenant, tc, "passed", category="Success", duration_sec=t.sec(), message="OK")
    except Exception as e:
        emit_shot(socketio, tenant, "nagative", f"{tc}_error")
        emit_case(socketio, tenant, tc, "failed", category="Success", duration_sec=t.sec(), message=str(e))
        raise
