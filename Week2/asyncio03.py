# Program 3: The Event Loop (asyncio.run)
# Concept: Using the Event Loop to actually execute a Coroutine Object.
import asyncio

async def greet():
    print("Hello from the Event loop!")

if __name__ == "__main__":
    coro_object = greet()
    asyncio.run(coro_object)  # This will execute the coroutine object and print the message
