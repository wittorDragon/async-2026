# Program 6: Creating a Concurrent Task
# Concept: Wrapping a coroutine inside asyncio.create_task() to schedule it to run in the background.
import asyncio
from time import ctime,time

async def cook_spahetti(customer):
    print(f"{ctime()} | -> Starting Cooking for Customer {customer}")
    await asyncio.sleep(1)  # Simulate cooking time
    print(f"{ctime()} | -> Finished Cooking for Customer {customer}")

async def main():
    start_time = time()
    
    # Create tasks for two customers
    task_a = asyncio.create_task(cook_spahetti("A"))

    print(f"{ctime()} | -> Main program can do other things while Task A runs in background.")
    
    # Wait for both tasks to complete and get their results
    await task_a

    print(f"Total time: {time() - start_time:0.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())  # This will execute the main coroutine and demonstrate extracting return values from tasks