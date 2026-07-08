# Objective: Label task objects explicitly to simplify logging and production tracking.
import asyncio
from time import ctime

async def background_worker():
    await asyncio.sleep(0.1)

async def main():
    task = asyncio.create_task(background_worker())
    
    # Defult auto-generated name assigned by Python framwork
    print(f"{ctime()} Initial Name: {task.get_name()}") # 
    
    # Override name with custom domain spacific tag
    task.set_name("Payment-Gateway-Validator")
    print(f"{ctime()} Updated Name: {task.get_name()}") # Expected: Payment-Gateway-Validator

asyncio.run(main())