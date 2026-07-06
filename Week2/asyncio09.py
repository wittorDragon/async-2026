# Program 9: Dynamically Tracking Tasks in a List
# Concept: Managing multiple generated tasks dynamically by appending them into a standard Python list.
import asyncio
from time import ctime,time

async def serve_customer(name):
    print(f"{ctime()} | -> Handling Customer {name}...")
    await asyncio.sleep(1)  # Simulate a delay in serving the customer
    print(f"{ctime()} | -> Done Customer {name}!")

async def main():
    start_time = time()
    customers = ["A", "B", "C", "D"]
    tasks_list = []  # List to hold the tasks

    for name in customers:
        t = asyncio.create_task(serve_customer(name))  # Create a task for each customer
        tasks_list.append(t)  # Append the task to the list

    for t in tasks_list:
        await t  # Await each task to ensure they complete

    print(f"served all {len(customers)} customers in {time() - start_time:0.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())  # This will execute the main coroutine and demonstrate dynamically tracking tasks in a list