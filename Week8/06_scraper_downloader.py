import asyncio

# Async function to scrape image links from web pages
async def link_scraper(queue: asyncio.Queue, page_urls: list[str]) -> None:
	"""Scan pages and place each discovered image URL into the queue."""
	print("[Producer] เริ่มสแกนหาลิงก์รูปภาพ...")

    # วนลูปผ่านรายการหน้าเว็บ
	for page in page_urls:
		print(f"  -- [Producer] สแกนหน้าเว็บ: {page}")
		await asyncio.sleep(0.3)

		for image_number in range(1, 3):
			image_url = (
				f"https://example.com/images/{page}_img{image_number}.jpg"
			)
			await queue.put(image_url)

	print("[Producer] สแกนหาลิงก์รูปภาพเสร็จสิ้น!\n")

# Async function to download images from the queue
async def image_downloader(queue: asyncio.Queue, worker_name: str) -> int:
	"""Download image URLs from the queue until a None sentinel is received."""
	downloaded_count = 0
	print(f"[{worker_name}] สตาร์ทเตรียมพร้อมโหลดรูป...")
    # Loop to download images from the queue until a None sentinel is received
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
	# 1. สร้างรายการของหน้าเว็บที่ต้องการสแกน
	pages = ["page_1", "page_2", "page_3"]
	queue: asyncio.Queue[str | None] = asyncio.Queue()
    # 2. สร้าง task สำหรับ producer และ consumer
	producer_task = asyncio.create_task(link_scraper(queue, pages))
	downloader_task = asyncio.create_task(
		image_downloader(queue, "Downloader_01")
	)
    # 3. รอให้ producer ทำงานเสร็จและรอให้คิวว่าง
	await producer_task
	await queue.join()
    # 4. ส่งสัญญาณ None ให้กับ consumer เพื่อให้หยุดทำงาน
	await queue.put(None)
	await downloader_task
    # 5. แสดงผลลัพธ์เมื่อทุกอย่างเสร็จสิ้น
	print("=== Web Scraper & Image Download ทำงานเสร็จสิ้น ===")


if __name__ == "__main__":
	asyncio.run(main())
