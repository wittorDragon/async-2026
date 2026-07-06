# Program 7: Dual Tasks Concurrency
# Concept: Scheduling two distinct tasks concurrently and awaiting them individually without gather.
import asyncio
from time import time,ctime

async def cook_spahetti(customer):
    print(f"{ctime()} | -> Starting Cooking for Customer {customer}")
    await asyncio.sleep(1)  # Simulate cooking time
    print(f"{ctime()} | -> Finished Cooking for Customer {customer}")

async def main():
    start_time = time()
    
    # Create tasks for two customers
    task_a = asyncio.create_task(cook_spahetti("A"))
    task_b = asyncio.create_task(cook_spahetti("B"))

    #print(f"{ctime()} | -> Main program can do other things while Task A and B run in background.")
    
    # Wait for both tasks to complete and get their results
    await task_a
    await task_b

    print(f"Total Operation Time: {time() - start_time:0.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())  # This will execute the main coroutine and demonstrate dual task concurrency