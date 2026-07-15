# foodcourt_02_gather.py
import asyncio
from time import time,ctime
from food_utils import send_order_to_kitchen

async def main():
    MY_STUDENT_ID = "6710301021"
    print(f"{ctime()} | --- [Task 2] Practice using gather to waitfor all group orders ---")
    start_time = time()

    t1 = asyncio.create_task(send_order_to_kitchen(MY_STUDENT_ID, "hainanese_chicken", "Chicken Rice"))
    t2 = asyncio.create_task(send_order_to_kitchen(MY_STUDENT_ID, "noodle", "Wonton Noodles"))
    t3 = asyncio.create_task(send_order_to_kitchen(MY_STUDENT_ID, "steak", "Sizzling Steak"))

    results = await asyncio.gather(t1, t2, t3)

    for dish in results:
        print(f"{ctime()} | [Pickup] Shop: {dish['shop']} | Menu: {dish['menu']} is ready!")

    print(f"{ctime()} | Total time: {time() - start_time:.2f} seconds (Equals to the slowest dish).")

asyncio.run(main())

