# Program 8: Task Interleaving (Context Switching)
# Concept: Watching a single thread switch back and forth between two different workflows using create_task.
import asyncio
from time import ctime

async def kitchen_crew():
    print(f"{ctime()} | -> [Chef] puts noodles in boiling water")
    await asyncio.sleep(1)  # Simulate cooking time
    print(f"{ctime()} | -> [Chef] strains the noodles!")

async def bar_crew():
    print(f"{ctime()} | -> [Bar] starts grinding coffee beans...")
    await asyncio.sleep(1)  # Simulate coffee making time
    print(f"{ctime()} | -> [Bar] pours espresso shot!")

async def main():
    # Create tasks for kitchen and bar crews
    task_kitchen = asyncio.create_task(kitchen_crew())
    task_bar = asyncio.create_task(bar_crew())

    # Wait for both tasks to complete
    await task_kitchen
    await task_bar

if __name__ == "__main__":
    asyncio.run(main())  # This will execute the main coroutine and demonstrate task interleaving