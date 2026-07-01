from time import time, ctime
import asyncio

async def greet_diners(customer):
    print(f"{ctime()} Greeting for Customer-{customer} ...")
    await asyncio.sleep(1)  # Simulating a time-consuming task
    print(f"{ctime()} Greeting for Customer-{customer} ...Done!")

async def customer_private_workflow(customer):
    # take_order(customer):
    print(f"{ctime()}   [Task-{customer}] Taking Order ...")
    await asyncio.sleep(1)  # Simulating a time-consuming task
    print(f"{ctime()}   [Task-{customer}] Taking Order ...Done!")
    # do_cooking(customer):
    print(f"{ctime()}   [Task-{customer}] Cooking spaghetti ...")
    await asyncio.sleep(1)  # Simulating a time-consuming task
    print(f"{ctime()}   [Task-{customer}] Cooking spaghetti ...Done!")
    # mini_bar(customer):
    print(f"{ctime()}   [Task-{customer}] Manage Bar for Drink ...")
    await asyncio.sleep(1)  # Simulating a time-consuming task
    print(f"{ctime()}   [Task-{customer}] Manage Bar for Drink ...Done!")
    print(f"{ctime()}   [Task-{customer}] All served!\n")

async def main():
    customers = ["A", "B", "C"]  # List of customers to serve
    start_time = time()

    for customer in customers:
        await greet_diners(customer)

    print(f"\n{ctime()} --- All Customers greeted. Splitting into individual tasks ---\n")

    # สร้าง task ทั้งหมดแล้วปล่อยให้รันพร้อมกันบน event loop เดียว
    tasks = [customer_private_workflow(customer) for customer in customers]
    await asyncio.gather(*tasks)

    duration = time() - start_time
    print(f"{ctime()} Finished Cooking in {duration:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())