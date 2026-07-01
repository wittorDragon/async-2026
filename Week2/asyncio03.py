# Program 3: The Event Loop (asyncio.run)
# Concept: Using the Event Loop to actually execute a Coroutine Object.
import asyncio

async def gree():
    print("Hello from the Event loop!")

if __name__=="__main__":
    coro_object = gree()
    asyncio.run(coro_object)