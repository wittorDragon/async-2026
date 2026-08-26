import asyncio


async def producer(queue: asyncio.Queue[str | None]) -> None:
	"""Create 20 coupons and put them into the shared queue."""
	total_coupons = 20
	print(f"[Producer] เริ่มสร้างคูปองจำนวน {total_coupons} ใบ...")

	for coupon_number in range(1, total_coupons + 1):
		coupon = f"COUPON-{coupon_number:02d}"
		await queue.put(coupon)
		print(f"  -- [Producer] สร้างและใส่คิวสำเร็จ: {coupon}")
		await asyncio.sleep(0.01)

	print("[Producer] สร้างคูปองเสร็จสิ้นเรียบร้อยแล้ว!\n")


async def consumer(
	queue: asyncio.Queue[str | None], consumer_name: str
) -> list[str]:
	"""Claim coupons until this consumer receives a None sentinel."""
	claimed_coupons: list[str] = []
	print(f"[{consumer_name}] เริ่มต้นรอรับคูปอง...")

    # Loop to claim coupons from the queue until a None sentinel is received
	
	while True:
		# ดึงคูปองจากคิว (รอถ้าไม่มีคูปอง)
		coupon = await queue.get()
        # ตรวจสอบว่าคูปองที่ดึงมาคือ None หรือไม่ (เป็นสัญญาณให้หยุดทำงาน)
		if coupon is None:
			queue.task_done()
			break

		claimed_coupons.append(coupon)
		print(
			f"-> [{consumer_name}] ได้รับคูปอง: {coupon} "
			f"(รวมสะสม: {len(claimed_coupons)} ใบ)"
		)
		# แจ้งให้คิวทราบว่าการดึงคูปองเสร็จสิ้นแล้ว
		await asyncio.sleep(0.04) # จำลองเวลาที่ใช้ในการประมวลผลคูปอง
		queue.task_done()

	print(
		f"[{consumer_name}] ทำงานเสร็จสิ้น! "
		f"รวมคูปองที่เก็บได้ทั้งหมด: {len(claimed_coupons)} ใบ"
	)
	return claimed_coupons

# Main function to run the producer and consumers
async def main() -> None:
	total_coupons = 20
	number_of_consumers = 2
	queue: asyncio.Queue[str | None] = asyncio.Queue()
    # Create tasks for the producer and consumers
	producer_task = asyncio.create_task(producer(queue))
	consumer_tasks = [
		asyncio.create_task(consumer(queue, f"Consumer_{consumer_number:02d}"))
		for consumer_number in range(1, number_of_consumers + 1)
	]

	await producer_task
	await queue.join()

    # ส่งสัญญาณ None ให้กับทุก consumer เพื่อให้พวกเขาหยุดทำงาน
	for _ in range(number_of_consumers):
		await queue.put(None)

    # รอให้ทุก consumer ทำงานเสร็จสิ้นและเก็บคูปองที่ได้รับ
	claimed_by_consumers = await asyncio.gather(*consumer_tasks)
	all_claimed_coupons = [
		coupon
		for claimed_coupons in claimed_by_consumers
		for coupon in claimed_coupons
	]
    # แสดงผลลัพธ์เมื่อทุกอย่างเสร็จสิ้น
	print("=== ระบบ Multi-Consumer ทำงานเสร็จสิ้น ===")
	print(
		f"รับคูปองครบ {len(all_claimed_coupons)}/{total_coupons} ใบ "
		f"โดยใช้ Consumer {number_of_consumers} ตัว"
	)


if __name__ == "__main__":
	asyncio.run(main())
