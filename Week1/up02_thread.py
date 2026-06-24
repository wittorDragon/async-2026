from time import sleep, ctime, time, process_time
import os
import threading
import psutil

# ============================================================
# ระบบจำลองกาแฟอัจฉริยะ - แบบ Multi-Threading
# ลูกค้า 3 คนเริ่มชงกาแฟพร้อมกัน (Thread ละ 1 คน)
# แต่ละลูกค้า: ชงกาแฟ 1 วินาที → แสดงผล LCD 1 วินาที
# ============================================================

# Lock สำหรับป้องกัน print ปนกัน
print_lock = threading.Lock()

def make_coffee(customer_name):
    pid         = os.getpid()
    thread_id   = threading.current_thread().native_id
    thread_name = threading.current_thread().name

    # --- ขั้นตอนที่ 1: ชงกาแฟ ---
    with print_lock:
        print(f"{ctime()} | [PID: {pid}] [TID: {thread_id}] [{thread_name}] "
              f"☕ กำลังชงกาแฟให้ลูกค้า {customer_name}...")
    sleep(1)
    with print_lock:
        print(f"{ctime()} | [PID: {pid}] [TID: {thread_id}] [{thread_name}] "
              f"✅ ชงกาแฟให้ลูกค้า {customer_name} เสร็จแล้ว!")

    # --- ขั้นตอนที่ 2: แสดงผล LCD ---
    with print_lock:
        print(f"{ctime()} | [PID: {pid}] [TID: {thread_id}] [{thread_name}] "
              f"🖥️  กำลังอัปเดตหน้าจอ LCD สำหรับลูกค้า {customer_name}...")
    sleep(1)
    with print_lock:
        print(f"{ctime()} | [PID: {pid}] [TID: {thread_id}] [{thread_name}] "
              f"✅ LCD อัปเดตสำเร็จ! ลูกค้า {customer_name} รับกาแฟได้เลย!")

def main():
    queue    = ['A', 'B', 'C']
    main_pid = os.getpid()
    main_tid = threading.current_thread().native_id

    print(f"{ctime()} | [Main PID: {main_pid}] [Main TID: {main_tid}] "
          f"=== เริ่มระบบกาแฟอัจฉริยะ แบบ Multi-Threading ===\n")

    start_time = time()
    start_cpu  = process_time()

    # สร้าง Thread ให้ลูกค้าทุกคนพร้อมกัน
    threads = []
    for customer in queue:
        t = threading.Thread(target=make_coffee, args=(customer,), name=f"Thread-{customer}")
        threads.append(t)

    # Start ทุก Thread พร้อมกัน
    for t in threads:
        t.start()

    # รอทุก Thread เสร็จ
    for t in threads:
        t.join()

    duration     = time() - start_time
    cpu_duration = process_time() - start_cpu

    process = psutil.Process(os.getpid())
    mem_mb  = process.memory_info().rss / (1024 * 1024)

    print("\n" + "=" * 60)
    print(f"[สรุปแบบ Multi-Threading]")
    print(f"  เวลาที่ใช้จริง  (Wall Time) : {duration:0.2f} วินาที")
    print(f"  เวลา CPU        (CPU Time)  : {cpu_duration:0.4f} วินาที")
    print(f"  หน่วยความจำ RAM             : {mem_mb:.2f} MB")
    print("=" * 60)
    print(f"💡 คาดว่าใช้เวลาประมาณ 2 วินาที (ทำงานพร้อมกัน)")

if __name__ == "__main__":
    main()