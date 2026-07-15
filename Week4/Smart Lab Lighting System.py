"""
Smart Lab Lighting System - Controller (VS Code)
==================================================
ติดตั้งไลบรารีก่อนรัน (เปิด Terminal ใน VS Code แล้วพิมพ์):
    python -m pip install aiohttp

รัน:
    python Lights.py
แล้วเลือกเมนู 1-4 ตามที่อาจารย์จะทดสอบ
"""

import asyncio
import aiohttp

BASE_URL = "http://172.16.2.117:8088"
STUDENT_ID = "6710301021"

# เรียงจากซ้ายไปขวาตามที่ระบุใน spec (light_1 -> light_4)
LIGHT_IDS = ["light_1", "light_2", "light_3", "light_4"]


class LabLightClient:
    def __init__(self, base_url: str = BASE_URL, student_id: str = STUDENT_ID):
        self.base_url = base_url.rstrip("/")
        self.student_id = student_id
        self._session: aiohttp.ClientSession | None = None

    async def __aenter__(self):
        self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self._session:
            await self._session.close()

    async def get_all_status(self) -> dict:
        url = f"{self.base_url}/api/{self.student_id}/lights"
        async with self._session.get(url) as resp:
            resp.raise_for_status()
            return await resp.json()

    async def set_light(self, light_id: str, status: str) -> dict:
        status = status.upper()
        if status not in ("ON", "OFF"):
            raise ValueError("status ต้องเป็น 'ON' หรือ 'OFF' เท่านั้น")
        url = f"{self.base_url}/api/{self.student_id}/lights/{light_id}"
        async with self._session.post(url, json={"status": status}) as resp:
            if resp.status == 404:
                data = await resp.json()
                raise ValueError(f"ไม่พบหลอดไฟ '{light_id}': {data.get('detail')}")
            if resp.status == 400:
                data = await resp.json()
                raise ValueError(f"สถานะไม่ถูกต้อง: {data.get('detail')}")
            resp.raise_for_status()
            return await resp.json()

    async def turn_on(self, light_id: str) -> dict:
        return await self.set_light(light_id, "ON")

    async def turn_off(self, light_id: str) -> dict:
        return await self.set_light(light_id, "OFF")

    async def reset_all(self) -> dict:
        url = f"{self.base_url}/api/{self.student_id}/lights/reset"
        async with self._session.delete(url) as resp:
            resp.raise_for_status()
            return await resp.json()


# ---------------------------------------------------------------
# 1) สั่งปิดหลอดไฟทั้งหมดที่ "เปิดอยู่" (เช็คสถานะก่อน แล้วปิดเฉพาะดวงที่ ON)
# ---------------------------------------------------------------
async def scenario_1_turn_off_all_on(client: LabLightClient):
    print("\n== [1] ปิดหลอดไฟทั้งหมดที่เปิดอยู่ ==")
    status = await client.get_all_status()
    on_lights = [lid for lid, info in status.items() if info["status"] == "ON"]

    if not on_lights:
        print("  ไม่มีดวงไหนเปิดอยู่เลย")
        return

    print(f"  พบดวงที่เปิดอยู่: {on_lights} -> กำลังปิดพร้อมกัน (concurrent)")
    results = await asyncio.gather(*(client.turn_off(lid) for lid in on_lights))
    for r in results:
        print(f"  {r['light_id']} -> {r['current_status']}")


# ---------------------------------------------------------------
# 2) เปิดไฟจากซ้ายไปขวา (light_1 -> light_4) แบบตามลำดับ (sequential)
#    รอให้ดวงก่อนหน้าเสร็จก่อน แล้วค่อยเปิดดวงถัดไป
# ---------------------------------------------------------------
async def scenario_2_left_to_right(client: LabLightClient):
    print("\n== [2] เปิดไฟจากซ้ายไปขวา (ตามลำดับ) ==")
    for light_id in LIGHT_IDS:
        result = await client.turn_on(light_id)
        print(f"  เปิดแล้ว: {result['light_id']} -> {result['current_status']}")


# ---------------------------------------------------------------
# 3) เปิดไฟตาม Hardware Delay (เปิดพร้อมกันทั้งหมด แล้วปล่อยให้แต่ละดวง
#    "ติด" ตามลำดับ delay ของมันเอง คือดวงที่ delay น้อยจะติดก่อน)
# ---------------------------------------------------------------
async def scenario_3_by_hardware_delay(client: LabLightClient):
    print("\n== [3] เปิดไฟพร้อมกัน แต่ละดวงจะติดตาม Hardware Delay ของตัวเอง ==")
    tasks = [asyncio.create_task(client.turn_on(light_id)) for light_id in LIGHT_IDS]

    # as_completed จะคืนผลลัพธ์ตามลำดับที่ "เสร็จจริง" ก่อน-หลัง
    # ซึ่งจะตรงกับลำดับ delay จากน้อยไปมาก (light_1:0.5 -> light_4:0.8 -> light_2:1.2 -> light_3:2.0)
    for coro in asyncio.as_completed(tasks):
        result = await coro
        print(f"  ติดแล้ว: {result['light_id']} -> {result['current_status']}")


# ---------------------------------------------------------------
# 4) ควบคุมเอง (Manual control) - โหมด interactive รับคำสั่งจากผู้ใช้
# ---------------------------------------------------------------
async def scenario_4_manual_control(client: LabLightClient):
    print("\n== [4] โหมดควบคุมเอง (พิมพ์ 'exit' เพื่อออก) ==")
    print(f"  ไฟที่ควบคุมได้: {', '.join(LIGHT_IDS)}")
    while True:
        light_id = input("  เลือกหลอดไฟ (เช่น light_1) หรือ 'status' หรือ 'exit': ").strip()

        if light_id.lower() == "exit":
            break

        if light_id.lower() == "status":
            status = await client.get_all_status()
            for lid, info in status.items():
                print(f"    {lid}: {info['name']} -> {info['status']}")
            continue

        if light_id not in LIGHT_IDS:
            print("  ไม่พบหลอดไฟนี้ ลองใหม่อีกครั้ง")
            continue

        state = input("  ต้องการเปิดหรือปิด? (ON/OFF): ").strip().upper()
        try:
            print(f"  กำลังส่งคำสั่ง... (รอ hardware delay)")
            result = await client.set_light(light_id, state)
            print(f"  สำเร็จ: {result['light_id']} -> {result['current_status']}")
        except ValueError as e:
            print(f"  เกิดข้อผิดพลาด: {e}")


# ---------------------------------------------------------------
# เมนูหลัก
# ---------------------------------------------------------------
async def main():
    async with LabLightClient() as client:
        while True:
            print("\n" + "=" * 50)
            print("เมนูควบคุมไฟห้องแล็บ")
            print("  1) ปิดหลอดไฟทั้งหมดที่เปิดอยู่")
            print("  2) เปิดไฟจากซ้ายไปขวา (ตามลำดับ)")
            print("  3) เปิดไฟตาม Hardware Delay (พร้อมกัน)")
            print("  4) ควบคุมเอง (manual)")
            print("  5) ดูสถานะไฟทั้งหมด")
            print("  0) ออกจากโปรแกรม")
            choice = input("เลือกเมนู: ").strip()

            if choice == "1":
                await scenario_1_turn_off_all_on(client)
            elif choice == "2":
                await scenario_2_left_to_right(client)
            elif choice == "3":
                await scenario_3_by_hardware_delay(client)
            elif choice == "4":
                await scenario_4_manual_control(client)
            elif choice == "5":
                status = await client.get_all_status()
                for lid, info in status.items():
                    print(f"  {lid}: {info['name']} -> {info['status']}")
            elif choice == "0":
                print("ออกจากโปรแกรม")
                break
            else:
                print("กรุณาเลือกเมนูที่ถูกต้อง")


if __name__ == "__main__":
    asyncio.run(main())