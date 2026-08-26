import asyncio


async def producer(queue: asyncio.Queue[str | None]) -> None:
	"""Create 20 coupons and put them into the shared queue."""
	total_coupons = 20
	print(f"[Producer] เริ่มสร้างคูปองจำนวน {total_coupons} ใบ...")

	for coupon_number in range(1, total_coupons + 1):
		coupon = f"COUPON-{coupon_number:02d}"
		await queue.put(coupon)
		print(f"  -- [Producer] สร้างและใส่คิวสำเร็จ: {coupon}")
		await asyncio.sleep(0.02)

	print("[Producer] สร้างคูปองเสร็จสิ้นเรียบร้อยแล้ว!\n")


async def consumer(
	queue: asyncio.Queue[str | None], consumer_name: str
) -> list[str]:
	"""Claim coupons from the queue until the None sentinel is received."""
	claimed_coupons: list[str] = []
	print(f"[{consumer_name}] เริ่มต้นรอรับคูปอง...")

	while True:
		coupon = await queue.get()

		if coupon is None:
			queue.task_done()
			break

		claimed_coupons.append(coupon)
		print(
			f"-> [{consumer_name}] ได้รับคูปอง: {coupon} "
			f"(รวมสะสม: {len(claimed_coupons)} ใบ)"
		)
		await asyncio.sleep(0.05)
		queue.task_done()

	print(
		f"[{consumer_name}] ทำงานเสร็จสิ้น! "
		f"รวมคูปองที่เก็บได้ทั้งหมด: {len(claimed_coupons)} ใบ"
	)
	return claimed_coupons


async def main() -> None:
	queue: asyncio.Queue[str | None] = asyncio.Queue()

	producer_task = asyncio.create_task(producer(queue))
	consumer_task = asyncio.create_task(consumer(queue, "Consumer_01"))

	await producer_task
	await queue.join()

	await queue.put(None)
	claimed_coupons = await consumer_task

	print(
		"=== ระบบ Coupon Producer-Consumer ทำงานเสร็จสิ้น ===\n"
		f"คูปองที่รับทั้งหมด {len(claimed_coupons)} ใบ: {claimed_coupons}"
	)


if __name__ == "__main__":
	asyncio.run(main())
