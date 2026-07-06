# Program 10: Extracting Return Values from Tasks
# Concept: Accessing returned results from completed Task objects using .result() or direct assignment.
import asyncio

async def calculate_bill(customer, base_price):
    print(f"Calculating receipt for Customer {customer}...")
    await asyncio.sleep(1)  # Simulate a delay in calculation
    final_price = base_price * 1.07  # Adding tax
    return final_price

async def main():
    # Creating tasks for each customer
    task_a = asyncio.create_task(calculate_bill("A", 100))
    task_b = asyncio.create_task(calculate_bill("B", 200))

    # Awaiting the completion of Task A and Task B
    result_a = await task_a
    result_b = await task_b

    print(f"\nFinal Bill for A: ${result_a:.2f}")
    print(f"Final Bill for B: ${result_b:.2f}")
    print(f"Combined Total Revenue: {result_a + result_b:.2f}")

if __name__ == "__main__":
    asyncio.run(main())  # This will execute the main coroutine and print the final bills and combined revenue.