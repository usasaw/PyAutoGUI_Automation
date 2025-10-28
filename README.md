# PyautoGUI
PyAutoGUI คือไลบรารี Python ที่ช่วยให้ควบคุมเมาส์และคีย์บอร์ดได้โดยอัตโนมัติผ่านการเขียนโปรแกรม ทำให้สามารถสร้างสคริปต์เพื่อทำงานซ้ำๆ บนคอมพิวเตอร์ได้

## วิธีติดตั้ง (Setup)
### BACKEND
```bash
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1  # หรือ source .venv/bin/activate บน Linux/Mac
pip install -r requirements.txt
python app.py
```
### FULLSTACK
สคริปต์ start/stop อัตโนมัติ ให้รัน Flask (PyAutoGUI) + React (Vite) พร้อมกันด้วย concurrently

**1. ติดตั้งตัวช่วยที่ root ของโปรเจกต์**
ที่โฟลเดอร์ automate-nss/ (root เดียวกับ frontend/ และ backend/)
```bash
npm i -D concurrently wait-on cross-env
```
**2. แก้ package.json (root)**
```bash
npm run setup # ติดตั้งของฝั่ง backend+frontend ครั้งแรก
npm run dev # รัน Flask + Vite พร้อมกัน (โหมดพัฒนา)
npm run preview #รัน Flask + Vite preview (หลัง build แล้ว)
npm run build #build ฝั่ง React
```
## รันเซิร์ฟเวอร์
**ครั้งแรก (หรือเวลาเปลี่ยนเครื่อง):**
```bash
cd D:\Counter_services\PyAutoGUI_Automation\automate-nss
npm install   # ติดตั้ง concurrently/wait-on/cross-env ของ root
npm run setup # สร้าง venv + ติดตั้ง backend + ติดตั้ง frontend
```
**พัฒนารอบถัดไป:**
```bash
npm run dev
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