# PyautoGUI
PyAutoGUI คือไลบรารี Python ที่ช่วยให้ควบคุมเมาส์และคีย์บอร์ดได้โดยอัตโนมัติผ่านการเขียนโปรแกรม ทำให้สามารถสร้างสคริปต์เพื่อทำงานซ้ำๆ บนคอมพิวเตอร์ได้
## Requirements
- Windows (ควบคุม POS / RDP)
- Python 3.13
- Node.js 20.x หรือ 22.x (แนะนำอย่าใช้ Node 23)
- Git
## Clone Project
```bash
git clone https://github.com/usasaw/PyAutoGUI_Automation.git
```
## FULLSTACK ครั้งแรก (setup ครบ frontend + backend)
```bash
cd automate-nss
npm install      # ติดตั้ง concurrently / wait-on / cross-env ฯลฯ ให้ root
npm run setup    # สร้าง backend\.venv + pip install + npm install ฝั่ง frontend
```
> สิ่งที่ `npm run setup` ทำ:
> `setup:venv:` สร้าง virtualenv ที่ `backend/.venv`
```text
python -m venv backend/.venv
```
> `setup:backend:` ใช้ python ใน `.venv` ติดตั้ง lib ทั้งหมดของ backend
```text
backend\.venv\Scripts\python.exe -m pip install -r backend/requirements.txt
```
`setup:frontend:` ลง dependencies ของ React
```text
cd frontend && npm install
```
เรียบร้อยแล้ว แปลว่า backend และ frontend พร้อมใช้งาน
## RUN FULLSTACK
หลัง setup เสร็จ (หรือครั้งถัดไปที่กลับมาทำงาน)
```bash
npm run dev
```
หลัง `npm run dev`:
-   Backend: [http://localhost:5000](http://localhost:5000)
-   Frontend: [http://localhost:5173](http://localhost:5173)
เข้าเบราว์เซอร์ที่ [http://localhost:5173](http://localhost:5173)  
คุณควรเห็น Dashboard (การ์ดผู้ว่าจ้าง, Summary, Log, Screenshot)
*กด Ctrl + C เพื่อหยุดทั้งคู่*
## FRONT-END (Setup) เท่านั้น
ใช้สำหรับ Dev UI / React เทสหน้าบ้าน โดยไม่รัน Python/Flask/Socket เลย
```bash
cd frontend
npm i #ครั้งแรกเท่านั้น
npm run dev
```
## BACK-END (Setup) เท่านั้น
ใช้สำหรับคนที่จะรัน PyAutoGUI, Flask, socket.io โดยไม่เปิด React dev server
```bash
cd backend

# ครั้งแรกเท่านั้น:
python -m venv .venv
.\.venv\Scripts\Activate.ps1    # ถ้าใช้ PowerShell บน Windows
pip install -r requirements.txt

# รันเซิร์ฟเวอร์:
.\.venv\Scripts\python.exe app.py # แนะนำ
หรือ
python app.py
```
## Scripts ที่มีใน root/package.json
```bash
npm run setup # ติดตั้งของฝั่ง backend+frontend ครั้งแรก
npm run dev # รัน Flask + Vite พร้อมกัน (โหมดพัฒนา)
npm run preview # รัน Flask + Vite preview (หลัง build แล้ว)
npm run build # build ฝั่ง React
```
# การติดตั้งส่วนอื่นๆ
เปิด PowerShell ใน backend แล้ว activate venv ก่อน
```bash
cd D:\Counter_services\PyAutoGUI_Automation\automate-nss\backend
.\.venv\Scripts\Activate.ps1 # virtualenv
```
**1. การหาตำแหน่งของหน้าจอ**
หาตำแหน่งแกน x , y ด้วยการกดปุ่ม **Space Bar** และยกเลิกการค้นหาด้วยการกดปุ่ม **ESC**
```bash
cd .\utils\  
python get_position.py
```
**2. การติดตั้งคีย์บอร์ด**
```bash
pip install keyboard
```