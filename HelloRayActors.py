# A simple example of distributed actors using ray - http://rllib.io/
# https://ray.readthedocs.io/en/latest/actors.html

import ray

@ray.remote
class Counter(object):
    def __init__(self):
        self.value = 0

    def increment(self):
        self.value += 1
        return self.value


if __name__ == "__main__":
    # Initialize runtime environment
    ray.init()

    # Simple usage
    a1 = Counter.remote()
    a2 = Counter.remote()

    a1.increment.remote()  # ray.get returns 1
    a1.increment.remote()  # ray.get returns 2
    a1.increment.remote()  # ray.get returns 3

    a2.increment.remote()  # ray.get returns 1

    # Create ten Counter actors.
    counters = [Counter.remote() for _ in range(10)]

    # Increment each Counter once and get the results.
    # These tasks all happen in parallel.
    results = ray.get([c.increment.remote() for c in counters])
    print(results)  # prints [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    # Increment the first Counter five times.
    # These tasks are executed serially and share state.
    results = ray.get([counters[0].increment.remote() for _ in range(5)])
    print(results)  # prints [2, 3, 4, 5, 6]
