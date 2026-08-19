import asyncio
import httpx

SERVER_IP = "172.20.56.253"
PORT = "8080"

SERVER_URL = f"http://{SERVER_IP}:{PORT}"

MY_STUDENT_ID = "6710301021"  # เปลี่ยนเป็นรหัสนักศึกษาของคุณ


async def hunt_coupons():

    async with httpx.AsyncClient() as client:

        print(f"[{MY_STUDENT_ID}] เริ่มภารกิจล่าคูปอง...")

        # ยิงขอคูปอง 5 ครั้ง เพื่อพยายามเก็บคูปองให้ได้มากที่สุด (สูงสุด 2 ใบต่อคน)
        for attempt in range(1, 6):

            try:

                res = await client.post(
                    f"{SERVER_URL}/claim",
                    json={
                        "student_id": MY_STUDENT_ID
                    },
                    timeout=5.0
                )

                data = res.json()

                status = data.get("status")

                print(
                    f"ครั้งที่ {attempt}: "
                    f"{status} -> "
                    f"{data.get('message', data.get('claimed_coupon'))}"
                )

                # หากได้ครบ 2 ใบแล้ว หรือคูปองหมด ให้หยุดยิง request เพิ่ม
                if status in [
                    "LIMIT_REACHED",
                    "OUT_OF_STOCK"
                ]:
                    break

            except Exception as e:
                print(f"เกิดข้อผิดพลาดในการเชื่อมต่อ: {e}")

            # พักก่อนยิง request ครั้งต่อไป เพื่อไม่ให้ server overload
            await asyncio.sleep(0.01)

        print("\nกำลังดึงข้อมูลคูปองของตนเอง...")

        try:

            res = await client.get(
                f"{SERVER_URL}/my-coupons/{MY_STUDENT_ID}"
            )

            if res.status_code == 200:

                summary = res.json()

                total = summary.get("total_claimed", 0)

                coupons = summary.get(
                    "claimed_coupons",
                    []
                )

                print(
                    f"สรุปผล {MY_STUDENT_ID} "
                    f"ได้รับคูปองรวม {total} ใบ -> {coupons}"
                )

            else:
                print(
                    f"ดึงข้อมูลไม่สำเร็จ "
                    f"Status Code: {res.status_code}"
                )

        except Exception as e:
            print(f"เกิดข้อผิดพลาด: {e}")

        print("\nกำลังดึงสรุปรายงานทั้งหมดจาก Server (/summary)...")

        try:

            res = await client.get(
                f"{SERVER_URL}/summary"
            )

            if res.status_code == 200:

                summary_all = res.json()

                remaining_stock = summary_all.get(
                    "remaining_stock",
                    "N/A"
                )

                claims = summary_all.get(
                    "student_claims",
                    {}
                )

                print(
                    f"จำนวนคูปองคงเหลือใน Server: "
                    f"{remaining_stock} ใบ"
                )

                print("รายการคูปองที่แต่ละคนได้รับ:")

                for sid, coupons in claims.items():

                    print(
                        f"- {sid}: "
                        f"{len(coupons)} ใบ -> "
                        f"{coupons}"
                    )

            else:
                print(
                    f"ดึงสรุปรายงานไม่สำเร็จ "
                    f"Status Code: {res.status_code}"
                )

        except Exception as e:
            print(f"ข้อผิดพลาดในการดึงรายงานรวม: {e}")


if __name__ == "__main__":
    asyncio.run(hunt_coupons())