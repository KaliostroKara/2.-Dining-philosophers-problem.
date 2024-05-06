import threading
import random
import time

PHILOSOPHER_COUNT = 5
forks = [threading.Lock() for _ in range(PHILOSOPHER_COUNT)]

def philosopher(num):
    while True:
        think(num)
        dine(num)

def think(num):
    print(f"Філософ {num} думає.")
    time.sleep(random.uniform(0.1, 0.5))

def dine(num):
    left_fork, right_fork = num, (num + 1) % PHILOSOPHER_COUNT
    if num == 0:
        left_fork, right_fork = right_fork, left_fork

    with forks[left_fork]:
        print(f"Філософ {num} взяв виделку {left_fork}.")
        if forks[right_fork].acquire(timeout=random.uniform(0.1, 0.2)):
            try:
                print(f"Філософ {num} взяв виделку {right_fork} і починає їсти.")
                time.sleep(random.uniform(0.1, 0.5))
            finally:
                forks[right_fork].release()
                print(f"Філософ {num} поклав виделку {right_fork}.")
        else:
            print(f"Філософ {num} не може взяти виделку {right_fork} і відпускає виделку {left_fork}.")
    print(f"Філософ {num} поклав виделку {left_fork} і продовжує думати.")

if __name__ == "__main__":
    philosophers = [threading.Thread(target=philosopher, args=(i,)) for i in range(PHILOSOPHER_COUNT)]

    for p in philosophers:
        p.start()

    for p in philosophers:
        p.join()
