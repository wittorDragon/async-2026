# Objective: Implement complex processing workflows based on task fulfillment conditions.
import asyncio
from time import ctime

async def network_probe(server_name, delay):
    await asyncio.sleep(delay)
    return f"Ping successful: {server_name}"

async def main():
    # asyncio.wait requires a set of instantiated task wrappers
    tasks = {
        asyncio.create_task(network_probe("Primary-Server", 2.0)),
        asyncio.create_task(network_probe("Backup-Server-1", 0.5)),
        asyncio.create_task(network_probe("Backup-Server-2", 1.0))
    }
    
    # Break execution flow immediately when the fastest node replies
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    
    print(f"{ctime()} Count of Tasks Done: {len(done)}")       # Expected: 1
    print(f"{ctime()} Count of Tasks Pending: {len(pending)}") # Expected: 2
    
    for finished_task in done:
        print(f"{ctime()} Fastest Task Result: {finished_task.result()}")
        
    # Clean up remaining pending tasks to prevent memory leaks
    for ongoing_task in pending:
        ongoing_task.cancel()

asyncio.run(main())