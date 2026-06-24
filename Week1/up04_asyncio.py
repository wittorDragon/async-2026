import asyncio
from time import ctime, time, process_time
import os
import threading
import psutil

# ============================================================
# ระบบจำลองกาแฟอัจฉริยะ - แบบ Asyncio
# Single thread เดียว บริหารลูกค้า 3 คนพร้อมกันด้วย Event Loop
# แต่ละลูกค้า: ชงกาแฟ 1 วินาที → แสดงผล LCD 1 วินาที
# ============================================================

async def make_coffee(customer_name):
    pid         = os.getpid()
    thread_id   = threading.current_thread().native_id
    thread_name = threading.current_thread().name

    # --- ขั้นตอนที่ 1: ชงกาแฟ (non-blocking) ---
    print(f"{ctime()} | [PID: {pid}] [TID: {thread_id}] [{thread_name}] "
          f"☕ กำลังชงกาแฟให้ลูกค้า {customer_name}...")
    await asyncio.sleep(1)  # yield control → Event Loop ไปทำงานอื่นได้
    print(f"{ctime()} | [PID: {pid}] [TID: {thread_id}] [{thread_name}] "
          f"✅ ชงกาแฟให้ลูกค้า {customer_name} เสร็จแล้ว!")

    # --- ขั้นตอนที่ 2: แสดงผล LCD (non-blocking) ---
    print(f"{ctime()} | [PID: {pid}] [TID: {thread_id}] [{thread_name}] "
          f"🖥️  กำลังอัปเดตหน้าจอ LCD สำหรับลูกค้า {customer_name}...")
    await asyncio.sleep(1)  # yield control อีกครั้ง
    print(f"{ctime()} | [PID: {pid}] [TID: {thread_id}] [{thread_name}] "
          f"✅ LCD อัปเดตสำเร็จ! ลูกค้า {customer_name} รับกาแฟได้เลย!")

async def main():
    main_pid = os.getpid()
    main_tid = threading.current_thread().native_id

    print(f"{ctime()} | [Main PID: {main_pid}] [Main TID: {main_tid}] "
          f"=== เริ่มระบบกาแฟอัจฉริยะ แบบ Asyncio ===\n")

    start_time = time()
    start_cpu  = process_time()

    # รวบรวม coroutine ของลูกค้าทุกคน แล้วให้ Event Loop จัดการ
    await asyncio.gather(
        make_coffee('A'),
        make_coffee('B'),
        make_coffee('C'),
    )

    duration     = time() - start_time
    cpu_duration = process_time() - start_cpu

    process = psutil.Process(os.getpid())
    mem_mb  = process.memory_info().rss / (1024 * 1024)

    print("\n" + "=" * 60)
    print(f"[สรุปแบบ Asyncio]")
    print(f"  เวลาที่ใช้จริง  (Wall Time) : {duration:0.2f} วินาที")
    print(f"  เวลา CPU        (CPU Time)  : {cpu_duration:0.4f} วินาที")
    print(f"  หน่วยความจำ RAM             : {mem_mb:.2f} MB")
    print("=" * 60)
    print(f"💡 คาดว่าใช้เวลาประมาณ 2 วินาที (Single-thread + Event Loop)")

if __name__ == "__main__":
    asyncio.run(main())