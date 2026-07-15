# Program 2: The Coroutine Object
# Concept: Seeing that calling an async def function creates an "Object" but does not execute it yet.
import asyncio

async def gree():
    print("Hello!")

coro_object = gree()
print(type(coro_object))
coro_object
