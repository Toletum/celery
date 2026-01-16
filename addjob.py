import time

from mycelery import add_numbers


def main():
    # Dispatch the task asynchronously using .delay()
    # This returns an AsyncResult object immediately
    print("Sending task to Celery...")
    result = add_numbers.delay(10, 25)

    # Check if the task is ready
    print(f"Task ID: {result.id}")

    # We can wait for the result (optional)
    while not result.ready():
        print("Waiting for task to complete...")
        time.sleep(1)

    # Get the actual value returned by the task
    final_value = result.get()
    print(f"Task finished! The result is: {final_value}")


if __name__ == "__main__":
    main()
