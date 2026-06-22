import sys

def evaluate_grade(score):
    """
    แปลงคะแนนเป็นเกรด พร้อมสาธิต GIL และ Concurrency vs Parallelism
    
    GIL (Global Interpreter Lock):
    - Python อนุญาตให้เธรดเดียวรัน Python bytecode ในเวลาใดขณะหนึ่ง
    - ทำให้ threading ไม่ได้ทำงานขนานแท้ (true parallelism) สำหรับ CPU-bound tasks
    - แต่ยังมีประโยชน์สำหรับ I/O-bound tasks (Concurrency)
    """
    # --- สาธิต Concurrency ด้วย Threading (I/O-bound simulation) ---
    results = []
    lock = threading.Lock()

    def io_bound_task(task_id, duration):
        """จำลอง I/O-bound: เธรดสลับกันรอ ไม่บล็อกกัน (GIL ถูก release ระหว่าง sleep)"""
        time.sleep(duration)  # GIL ถูก release ตรงนี้ → เธรดอื่นวิ่งได้
        with lock:
            results.append(f"IO Task {task_id} done")

    threads = [threading.Thread(target=io_bound_task, args=(i, 0.01)) for i in range(3)]
    t0 = time.time()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    io_time = time.time() - t0  # ~0.01s เพราะทำงาน concurrent จริง

    # --- สาธิต GIL บล็อก CPU-bound Threading ---
    counter = [0]

    def cpu_bound_task():
        """CPU-bound: GIL ไม่ถูก release → เธรดสลับกันรัน ไม่ขนานแท้"""
        for _ in range(100_000):
            counter[0] += 1  # GIL ถูกถือไว้ตลอด → bottleneck

    cpu_threads = [threading.Thread(target=cpu_bound_task) for _ in range(2)]
    t1 = time.time()
    for t in cpu_threads:
        t.start()
    for t in cpu_threads:
        t.join()
    cpu_thread_time = time.time() - t1

def main():
    # เปลี่ยนจาก > 2 เป็น > 1 เพื่อรองรับระบบ arguments ของ VPL
    if len(sys.argv) > 1:
        # sys.argv[-1] จะดึงอาร์กิวเมนต์ตัวสุดท้ายเสมอ (ซึ่งก็คือตัวเลขคะแนน เช่น 64, 45)
        test_score = int(sys.argv[-1])
        result = evaluate_grade(test_score)
        print(result) # พ่นเฉพาะผลลัพธ์ดิบให้ VPL จับคู่ตรวจสอบ
    else:
        # หากนักเรียนกดรันธรรมดา (ไม่มี arguments)
        test_score = 85
        result = evaluate_grade(test_score)
        print(f"Score: {test_score} -> Grade: {result}")

if __name__ == "__main__":
    main()