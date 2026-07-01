# Program 8: Task Interleaving (Context Switching)
# Concept: Watching a single thread switch back and forth between two different workflows using create_task.
import asyncio
from time import ctime

async def kitchen_crew():
    print(f"{ctime()} -> [Chef] puts noodle in boling water")
    await asyncio,sleep(1)
    print(f"{ctime()} -> [Chef] strains the noodler")

async def bar_crew():
    print(f"{ctime()} -> [Bar] puts noodle in boling water")
    await asyncio,sleep(1)
    print(f"{ctime()} -> [Bar] strains the noodler")

async def main():
    task_kitchen = asyncio.create_task(kitchen_crew)
    task_bar = asyncio.create_task(bar_crew)
    
    
    await task_kitchen
    await task_bar
    
if __name__=="__main__":
    asyncio.run(main())
   