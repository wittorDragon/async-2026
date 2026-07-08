# Objective: Learn how to query the lifecycle status of a task object.
import asyncio
from time import ctime

async def short_job():
    await asyncio.sleep(1)
    return "Success"

async def main():
    task = asyncio.create_task(short_job())
    
    # Inspect status immediately while it is still running
    print(f"{ctime()} Is task done? {task.done()}")          # Expected: False
    print(f"{ctime()} Is task canceled? {task.cancelled()}")  # Expected: False
    
    await task # Wait for completion
    
    # Inspect status again after it finishes
    print(f"{ctime()} Is task done now? {task.done()}")      # Expected: True
    print(f"{ctime()} Is task canceled now? {task.cancelled()}") # Expected: False

asyncio.run(main())