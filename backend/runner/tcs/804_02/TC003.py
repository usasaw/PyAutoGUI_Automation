import time, pyautogui as pag
from . import __name__ as pkgname
from ...pyauto_core import emit_log, emit_case, emit_shot, step_timer

def run(socketio, ctx):
    tenant = ctx["tenant"]
    tc = ctx.get("tc", "TC003 Search Tenant")
    emit_log(socketio, tenant, f"=== {tc} start (tenant={tenant}) ===")
    t = step_timer()

    try:
        time.sleep(2)
        pag.click(59, 265)
        emit_log(socketio, tenant, f"คลิกปุ่ม Counter Service")

        time.sleep(8)
        pag.click(444, 144)
        emit_log(socketio, tenant, f"คลิกปุ่ม ค้นหาผู้ว่าจ้าง สำเร็จ")

        time.sleep(5)
        # pag.click(142, 309)
        # pag.write("ไทยแอร์", interval=0.5)
        pag.click(618, 516 , interval=0.1)
        pag.click(71, 475 , interval=0.1)
        pag.click(65, 515 , interval=0.1)
        pag.click(744, 474 , interval=0.1)
        pag.click(440, 516 , interval=0.1)
        pag.click(108, 513 , interval=0.1)
        pag.click(538, 471 , interval=0.1)
        pag.click(704, 476 , interval=0.1)
        pag.click(444, 520 , interval=0.1)
        pag.click(705, 478 , interval=0.1)
        pag.click(450, 395 , interval=0.1)
        pag.click(660, 390 , interval=0.1)
        pag.click(64, 518)        
        emit_log(socketio, tenant, f"คีย์ ไทยแอร์ ในช่องค้นหาสำเร็จ")
        emit_shot(socketio, tenant, "result", "Search_tanent")
        socketio.sleep(0)

        time.sleep(1)
        pag.click(701, 309)
        emit_log(socketio, tenant, f"คลิกปุ่ม ค้นหา สำเร็จ")
        
        time.sleep(2)
        emit_shot(socketio, tenant, "result", f"Tenant_Thai_Air")
        socketio.sleep(0)
        pag.click(219, 215)
        emit_log(socketio, tenant, f"คลิกผู้ว่าจ้าง ไทยแอร์เอเชีย สำเร็จ")

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

        time.sleep(20)
        emit_shot(socketio, tenant, "result", "Detail_page_TaxID_SV")
        socketio.sleep(0)

        time.sleep(2)
        pag.press("esc")

    except Exception as e:
        emit_shot(socketio, tenant, "nagative", f"{tc}_error")
        emit_case(socketio, tenant, tc, "faild", category="Nagative Search", duration_sec=t.sec(), message=str(e))
        raise