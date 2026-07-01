from time import sleep, time, ctime
import threading

def greet_diners(customer):
    print(f"{ctime()} -> Greeting for Customer-{customer}...")
    sleep(1)  # Simulating a time-consuming task
    print(f"{ctime()} -> Greeting for Customer-{customer}...Done!")

def customer_private_workflow(customer):

    #take_order(customer):
    print(f"{ctime()} [Thread-{customer}] Taking Order...")
    sleep(1)  # Simulating a time-consuming task
    print(f"{ctime()} [Thread-{customer}] Taking Order...Done!")

    #do_cooking(customer):
    print(f"{ctime()} [Thread-{customer}] Cooking spaghetti...")
    sleep(1)  # Simulating a time-consuming task
    print(f"{ctime()} [Thread-{customer}] Cooking spaghetti...Done!")

    #mini_bar(customer):
    print(f"{ctime()} [Thread-{customer}] Manage Bar for Drink...")
    sleep(1)  # Simulating a time-consuming task
    print(f"{ctime()} [Thread-{customer}] Manage Bar for Drink...Done!")
    print(f"{ctime()} [Thread-{customer}] All served!\n")


if __name__ == "__main__":
    customers = ["A", "B", "C"]  # List of customers to serve
    start_time = time()

    for customer in customers:
        greet_diners(customer)
    print(f"\n{ctime()} === All Customers greeted. Splitting into individual threads ===\n")
    customer_threads = []
    for customer in customers:
        t = threading.Thread(target=customer_private_workflow, args=(customer,))
        customer_threads.append(t)
        t.start()

    for t in customer_threads:
        t.join()

    duration = time() - start_time
    print(f"{ctime()} Finished Cooking in {duration:.2f} seconds")