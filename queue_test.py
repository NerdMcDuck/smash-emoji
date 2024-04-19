import threading
import queue
from typing import List


def process_input_worker(blocking_q: queue.Queue, test_arg: str):
    """
    A thread worker to process enqueued items.
    :param blocking_q:
    :param test_arg:
    :return:
    """
    print(f"{test_arg=}\n")

    while True:
        item = blocking_q.get()
        print(f'Working on {item}')
        print(f'Finished {item}')
        print(f"items remaining in queue {blocking_q.qsize()}")
        blocking_q.task_done()


def main():
    q = queue.Queue(maxsize=5)

    # Turn-on the worker thread.
    threading.Thread(
        target=process_input_worker, daemon=True, args=(q, "arg from main()")).start()

    while 1:

        user_input = input("Enter up to 5 spaced separated emoji commands: ")
        usr_input_lst: List[str] = user_input.split(" ")

        if "stop" in usr_input_lst:
            print("Thanks for playing!")
            break

        print(f"{user_input=}")

        # Send the user input task requests to the worker.
        for item in usr_input_lst:
            q.put(item)

        # Block until all tasks are done.
        q.join()


if __name__ == '__main__':
    main()
