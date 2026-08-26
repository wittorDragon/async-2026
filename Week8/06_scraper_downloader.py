import asyncio


async def link_scraper(queue: asyncio.Queue, page_urls: list[str]) -> None:
	"""Scan pages and place each discovered image URL into the queue."""
	print("[Producer] เริ่มสแกนหาลิงก์รูปภาพ...")

	for page in page_urls:
		print(f"  -- [Producer] สแกนหน้าเว็บ: {page}")
		await asyncio.sleep(0.3)

		for image_number in range(1, 3):
			image_url = (
				f"https://example.com/images/{page}_img{image_number}.jpg"
			)
			await queue.put(image_url)

	print("[Producer] สแกนหาลิงก์รูปภาพเสร็จสิ้น!\n")


async def image_downloader(queue: asyncio.Queue, worker_name: str) -> int:
	"""Download image URLs from the queue until a None sentinel is received."""
	downloaded_count = 0
	print(f"[{worker_name}] สตาร์ทเตรียมพร้อมโหลดรูป...")

	while True:
		image_url = await queue.get()

		if image_url is None:
			queue.task_done()
			break

		downloaded_count += 1
		print(
			f"-> [{worker_name}] (รูปที่ {downloaded_count}) "
			f"กำลังโหลด: {image_url}"
		)
		await asyncio.sleep(0.5)
		queue.task_done()

	print(
		f"[{worker_name}] ทำงานเสร็จสิ้น! "
		f"ดาวน์โหลดรวมทั้งหมด {downloaded_count} รูป"
	)
	return downloaded_count


async def main() -> None:
	pages = ["page_1", "page_2", "page_3"]
	queue: asyncio.Queue[str | None] = asyncio.Queue()

	producer_task = asyncio.create_task(link_scraper(queue, pages))
	downloader_task = asyncio.create_task(
		image_downloader(queue, "Downloader_01")
	)

	await producer_task
	await queue.join()

	await queue.put(None)
	await downloader_task

	print("=== Web Scraper & Image Download ทำงานเสร็จสิ้น ===")


if __name__ == "__main__":
	asyncio.run(main())
