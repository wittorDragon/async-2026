import asyncio
from typing import List, Dict
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

STUDENTS = ["6710301031","6710301021","6710301042","6710301045","6710301049","6710301051"]
GROUP_SIZE = len(STUDENTS)
TOTAL_COUPONS = (GROUP_SIZE * 2) - 1  # จำนวนคูปองทั้งหมดที่สามารถแจกได้

coupons_db: list[str] = [f"COUPON-{i:02d}" for i in range(1, TOTAL_COUPONS + 1)]  # สร้างคูปองทั้งหมด

current_coupon_index = 0

stundent_claims: Dict[str, List[str]] = {student_id: [] for student_id in STUDENTS}  # เก็บคูปองที่นักเรียนแต่ละคนเคย claim แล้ว
coupon_lock = asyncio.Lock()
class ClaimRequest(BaseModel):
    student_id: str

@app.post("/claim")
async def claim_coupon(request: ClaimRequest):
    global current_coupon_index

    student_id = request.student_id
    async with coupon_lock:

        if student_id not in STUDENTS:
            return {"status": "INVALID", "message": "Invalid student ID."}

        if len(stundent_claims[student_id]) >= 2:
            return {"status": "LIMIT_REACHED", "message": "You have already claimed the maximum number of coupons."}

        if current_coupon_index < len(coupons_db):
            index_to_claim = current_coupon_index

            await asyncio.sleep(0.2475)  # Simulate some processing delay

            coupon = coupons_db[index_to_claim]
            stundent_claims[student_id].append(coupon)

            current_coupon_index  = index_to_claim + 1  # Move to the next coupon

            return {"status": "SUCCESS", "claimed_coupon": coupon, "total_owned": len(stundent_claims[student_id])}
    
    return {"status": "SOLD_OUT", "message": "All coupons have been claimed."}
    