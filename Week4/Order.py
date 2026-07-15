"""
Async Food Ordering Simulation
================================
สาธิตแนวคิด asyncio หลัก ๆ ผ่านการจำลองการสั่งอาหาร โดยแต่ละเมนูมี
"เวลาทำอาหาร" (simulated delay) ต่างกัน:

    ข้าวมันไก่ (Chicken Rice) : 0.8s
    ก๋วยเตี๋ยว  (Noodle)       : 1.5s
    สเต็ก      (Steak)         : 4.0s

Task 1 - Create Task     : สั่งข้าวมันไก่เดี่ยว ๆ ผ่าน create_task -> ต้อง < 1.2s
Task 2 - Gather           : สั่ง 3 เมนูพร้อมกัน -> เวลารวมต้อง = เมนูที่ช้าที่สุด (สเต็ก 4.0s)
                            ต้องอยู่ในช่วง 3.8s - 4.5s (ถ้า sequential จะได้ 6.3s ซึ่ง FAIL)
Task 3 - Wait (FIRST_COMPLETED): แข่งกัน 3 เมนู ตัวที่เสร็จก่อน (ข้าวมันไก่) ต้อง
                            ปลดบล็อกทันทีที่ 0.8s -> ต้อง < 1.2s
Task 5 - Mix Concepts     : ก๋วยเตี๋ยว (1.5s) + ข้าวมันไก่ที่มี timeout (0.8s) รันผ่าน gather
                            -> เวลารวมต้อง = งานที่ช้ากว่า (1.5s) อยู่ในช่วง 1.4s - 1.9s
"""

import asyncio
import time


# ---------- Simulated "kitchen" ----------

async def prepare_dish(name: str, delay: float) -> str:
    """จำลองการทำอาหาร ใช้เวลา `delay` วินาที"""
    await asyncio.sleep(delay)
    return f"{name} พร้อมเสิร์ฟ (ใช้เวลา {delay}s)"


DISHES = {
    "chicken_rice": 0.8,
    "noodle": 1.5,
    "steak": 4.0,
}


def _report(task_name: str, elapsed: float, low: float, high: float):
    status = "PASS ✅" if low <= elapsed <= high else "FAIL ❌"
    print(f"  เวลาที่ใช้: {elapsed:.3f}s  (เกณฑ์: {low}s - {high}s)  -> {status}")


# ---------- Task 1: Create Task ----------

async def task1_create_task():
    print("\n== Task 1: Create Task (สั่งข้าวมันไก่เดี่ยว ๆ) ==")
    start = time.perf_counter()

    task = asyncio.create_task(prepare_dish("ข้าวมันไก่", DISHES["chicken_rice"]))
    result = await task

    elapsed = time.perf_counter() - start
    print(f"  ผลลัพธ์: {result}")
    # เกณฑ์: strict limit < 1.2s
    _report("task1", elapsed, 0.0, 1.2)


# ---------- Task 2: Gather (concurrent) ----------

async def task2_gather():
    print("\n== Task 2: Gather (สั่ง 3 เมนูพร้อมกัน) ==")
    start = time.perf_counter()

    results = await asyncio.gather(
        prepare_dish("ข้าวมันไก่", DISHES["chicken_rice"]),
        prepare_dish("ก๋วยเตี๋ยว", DISHES["noodle"]),
        prepare_dish("สเต็ก", DISHES["steak"]),
    )

    elapsed = time.perf_counter() - start
    for r in results:
        print(f"  {r}")
    # เกณฑ์: ต้องเท่ากับเมนูที่ช้าที่สุด (สเต็ก 4.0s) อยู่ในช่วง 3.8 - 4.5s
    _report("task2", elapsed, 3.8, 4.5)


# ---------- Task 3: Wait (FIRST_COMPLETED) ----------

async def task3_wait_first():
    print("\n== Task 3: Wait First (แข่งกัน 3 เมนู เอาที่เสร็จก่อน) ==")
    start = time.perf_counter()

    tasks = [
        asyncio.create_task(prepare_dish("ข้าวมันไก่", DISHES["chicken_rice"])),
        asyncio.create_task(prepare_dish("ก๋วยเตี๋ยว", DISHES["noodle"])),
        asyncio.create_task(prepare_dish("สเต็ก", DISHES["steak"])),
    ]

    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    elapsed = time.perf_counter() - start
    for d in done:
        print(f"  เสร็จก่อน: {d.result()}")

    # ยกเลิกงานที่เหลือ (ยังไม่เสร็จ) เพื่อไม่ให้ค้างอยู่เบื้องหลัง
    for p in pending:
        p.cancel()
    await asyncio.gather(*pending, return_exceptions=True)

    # เกณฑ์: ข้าวมันไก่ (เร็วสุด) ต้องปลดบล็อกทันทีที่ 0.8s -> strict limit < 1.2s
    _report("task3", elapsed, 0.0, 1.2)


# ---------- Task 5: Mix Concepts (Gather + wait_for/timeout) ----------

async def chicken_rice_with_timeout(timeout: float = 2.0) -> str:
    """สั่งข้าวมันไก่ แต่มีการจำกัดเวลาด้วย wait_for (timeout)"""
    try:
        return await asyncio.wait_for(
            prepare_dish("ข้าวมันไก่ (มี timeout)", DISHES["chicken_rice"]),
            timeout=timeout,
        )
    except asyncio.TimeoutError:
        return "ข้าวมันไก่: หมดเวลารอ (timeout)"


async def task5_mix_concepts():
    print("\n== Task 5: Mix Concepts (Gather + wait_for) ==")
    start = time.perf_counter()

    results = await asyncio.gather(
        prepare_dish("ก๋วยเตี๋ยว", DISHES["noodle"]),
        chicken_rice_with_timeout(timeout=2.0),
    )

    elapsed = time.perf_counter() - start
    for r in results:
        print(f"  {r}")
    # เกณฑ์: เท่ากับงานที่ช้ากว่า (ก๋วยเตี๋ยว 1.5s) อยู่ในช่วง 1.4 - 1.9s
    _report("task5", elapsed, 1.4, 1.9)


# ---------- Runner ----------

async def main():
    await task1_create_task()
    await task2_gather()
    await task3_wait_first()
    await task5_mix_concepts()


if __name__ == "__main__":
    asyncio.run(main())