# Program 1: The First Coroutine Function
# Concept: Understanding async def and how it differs from a normal function.

import asyncio

async def greet():
    print("Hello From coroutine!")
    
    
print(type(greet)) # <class 'function'>