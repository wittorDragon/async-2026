from time import sleep, ctime, time, process_time
import os
import threading
import psutil

# ============================================================
# ระบบจำลองกาแฟอัจฉริยะ - แบบ Synchronous
# แต่ละลูกค้า: ชงกาแฟ 1 นาที → แสดงผล LCD 1 นาที (รวม 2 นาที)
# ============================================================

def make_coffee(customer_name):
    pid        = os.getpid()
    thread_id  = threading.current_thread().native_id
    thread_name = threading.current_thread().name

    # --- ขั้นตอนที่ 1: ชงกาแฟ ---
    print(f"{ctime()} | [PID: {pid}] [TID: {thread_id}] [{thread_name}] "
          f"☕ กำลังชงกาแฟให้ลูกค้า {customer_name}...")
    sleep(1)  # ชงกาแฟ 1 วินาที (จำลองแทน 1 นาที)
    print(f"{ctime()} | [PID: {pid}] [TID: {thread_id}] [{thread_name}] "
          f"✅ ชงกาแฟให้ลูกค้า {customer_name} เสร็จแล้ว!")

    # --- ขั้นตอนที่ 2: แสดงผล LCD ---
    print(f"{ctime()} | [PID: {pid}] [TID: {thread_id}] [{thread_name}] "
          f"🖥️  กำลังอัปเดตหน้าจอ LCD สำหรับลูกค้า {customer_name}...")
    sleep(1)  # อัปเดต LCD 1 วินาที (จำลองแทน 1 นาที)
    print(f"{ctime()} | [PID: {pid}] [TID: {thread_id}] [{thread_name}] "
          f"✅ LCD อัปเดตสำเร็จ! ลูกค้า {customer_name} รับกาแฟได้เลย!")

def main():
    queue    = ['A', 'B', 'C']
    main_pid = os.getpid()
    main_tid = threading.current_thread().native_id

    print(f"{ctime()} | [Main PID: {main_pid}] [Main TID: {main_tid}] "
          f"=== เริ่มระบบกาแฟอัจฉริยะ แบบ Synchronous ===\n")

    start_time = time()
    start_cpu  = process_time()

    for customer in queue:
        make_coffee(customer)
        print()

    duration     = time() - start_time
    cpu_duration = process_time() - start_cpu

    process = psutil.Process(os.getpid())
    mem_mb  = process.memory_info().rss / (1024 * 1024)

    print("=" * 60)
    print(f"[สรุปแบบ Synchronous]")
    print(f"  เวลาที่ใช้จริง  (Wall Time) : {duration:0.2f} วินาที")
    print(f"  เวลา CPU        (CPU Time)  : {cpu_duration:0.4f} วินาที")
    print(f"  หน่วยความจำ RAM             : {mem_mb:.2f} MB")
    print("=" * 60)
    print(f"💡 คาดว่าใช้เวลาประมาณ 6 วินาที (3 คน × 2 วินาที = 6 วินาที)")

if __name__ == "__main__":
    main()