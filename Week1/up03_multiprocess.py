from time import sleep, ctime, time, process_time
import os
import threading
import multiprocessing
import psutil

# ============================================================
# ระบบจำลองกาแฟอัจฉริยะ - แบบ Multi-Processing
# ลูกค้า 3 คน แต่ละคนได้ Process แยกอิสระของตัวเอง
# แต่ละลูกค้า: ชงกาแฟ 1 วินาที → แสดงผล LCD 1 วินาที
# ============================================================

def make_coffee(customer_name):
    pid         = os.getpid()
    thread_id   = threading.current_thread().native_id
    thread_name = threading.current_thread().name

    # --- ขั้นตอนที่ 1: ชงกาแฟ ---
    print(f"{ctime()} | [PID: {pid}] [TID: {thread_id}] [{thread_name}] "
          f"☕ กำลังชงกาแฟให้ลูกค้า {customer_name}...", flush=True)
    sleep(1)
    print(f"{ctime()} | [PID: {pid}] [TID: {thread_id}] [{thread_name}] "
          f"✅ ชงกาแฟให้ลูกค้า {customer_name} เสร็จแล้ว!", flush=True)

    # --- ขั้นตอนที่ 2: แสดงผล LCD ---
    print(f"{ctime()} | [PID: {pid}] [TID: {thread_id}] [{thread_name}] "
          f"🖥️  กำลังอัปเดตหน้าจอ LCD สำหรับลูกค้า {customer_name}...", flush=True)
    sleep(1)
    print(f"{ctime()} | [PID: {pid}] [TID: {thread_id}] [{thread_name}] "
          f"✅ LCD อัปเดตสำเร็จ! ลูกค้า {customer_name} รับกาแฟได้เลย!", flush=True)

def main():
    queue    = ['A', 'B', 'C']
    main_pid = os.getpid()
    main_tid = threading.current_thread().native_id

    print(f"{ctime()} | [Main PID: {main_pid}] [Main TID: {main_tid}] "
          f"=== เริ่มระบบกาแฟอัจฉริยะ แบบ Multi-Processing ===\n")

    start_time = time()
    start_cpu  = process_time()

    # สร้าง Process ให้ลูกค้าทุกคน
    processes = []
    for customer in queue:
        p = multiprocessing.Process(target=make_coffee, args=(customer,), name=f"Process-{customer}")
        processes.append(p)

    # Start ทุก Process พร้อมกัน
    for p in processes:
        p.start()

    # รอทุก Process เสร็จ
    for p in processes:
        p.join()

    duration     = time() - start_time
    cpu_duration = process_time() - start_cpu

    # วัด RAM ของ Main Process
    process = psutil.Process(os.getpid())
    mem_mb  = process.memory_info().rss / (1024 * 1024)

    print("\n" + "=" * 60)
    print(f"[สรุปแบบ Multi-Processing]")
    print(f"  เวลาที่ใช้จริง  (Wall Time) : {duration:0.2f} วินาที")
    print(f"  เวลา CPU        (CPU Time)  : {cpu_duration:0.4f} วินาที")
    print(f"  หน่วยความจำ RAM (Main)      : {mem_mb:.2f} MB")
    print("=" * 60)
    print(f"💡 คาดว่าใช้เวลาประมาณ 2 วินาที (แต่ละคนได้ Process แยก)")

if __name__ == "__main__":
    main()