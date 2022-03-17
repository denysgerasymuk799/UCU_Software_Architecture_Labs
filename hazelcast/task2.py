import hazelcast

from multiprocessing import Process


def racy_update(number):
    hz = hazelcast.HazelcastClient()

    # Create Distributed Map
    map = hz.get_map("distributed_map2").blocking()
    key = "1"
    map.put(key, 0)

    print(f"Process {number} -- Starting")
    for k in range(0, 1000):
        if k % 100 == 0:
            print(f"Process {number} -- At: {k}")

        value = map.get(key)
        value += 1
        map.put(key, value)

    print(f"Process {number} -- Finished! Result = {map.get(key)}")


def pessimistic_update(number):
    hz = hazelcast.HazelcastClient()

    # Get Distributed Map
    map = hz.get_map("distributed_map2").blocking()
    key = "1"
    map.put(key, 0)

    print(f"Process {number} -- Starting")
    for k in range(0, 1000):
        map.lock(key)
        try:
            value = map.get(key)
            value += 1
            map.put(key, value)
        finally:
            map.unlock(key)

    print(f"Process {number} -- Finished! Result = {map.get(key)}")


def optimistic_update(number):
    hz = hazelcast.HazelcastClient()

    # Get Distributed Map
    map = hz.get_map("distributed_map2").blocking()
    key = "1"
    map.put(key, 0)

    print(f"Process {number} -- Starting")
    for k in range(0, 1000):
        if k % 10 == 0:
            print(f"Process {number} -- At: {k}")

        while True:
            old_value = map.get(key)
            new_value = old_value
            new_value += 1
            if map.replace_if_same(key, old_value, new_value):
                break

    print(f"Process {number} -- Finished! Result = {map.get(key)}")


if __name__ == '__main__':
    numbers = [1, 2, 3]
    procs = []

    for index, number in enumerate(numbers):
        proc = Process(target=pessimistic_update, args=(number,))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()
