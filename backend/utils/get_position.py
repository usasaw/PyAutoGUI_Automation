import pyautogui as pag
import keyboard

def main():
    print("🖱️ จ่อเมาส์ไว้ที่ตำแหน่งที่ต้องการแล้วกด SPACE = แสดงพิกัด, กด ESC = หยุด\n")
    while True:
        if keyboard.is_pressed("space"):
            x, y = pag.position()
            print(f"คลิกที่: X={x}, Y={y}")
            while keyboard.is_pressed("space"):  # กันกดค้างแล้ว spam
                pass
        elif keyboard.is_pressed("esc"):
            print("หยุดโปรแกรมแล้ว")
            break

if __name__ == "__main__":
    main()
