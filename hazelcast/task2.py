import time
import hazelcast

from multiprocessing import Process


class Value:
    amount = 0


def racy_update(number):
    hz = hazelcast.HazelcastClient()

    # Create Distributed Map
    map = hz.get_map("distributed_map2").blocking()
    key = "1"
    map.put(key, Value())

    def put_callback(f):
        return f.result()

    print(f"Process {number} -- Starting")
    for k in range(0, 1000):
        if k % 100 == 0:
            print(f"Process {number} -- At: {k}")
        value = map.get(key).add_done_callback(put_callback)
        time.sleep(0.01)
        value.amount += 1
        map.put(key, value)

    print(f"Process {number} -- Finished! Result = {map.get(key).amount}")


def optimistic_update(number):
    hz = hazelcast.HazelcastClient()

    # Create Distributed Map
    map = hz.get_map("distributed_map2").blocking()
    key = "1"
    map.put(key, Value())

    print(f"Process {number} -- Starting")
    for k in range(0, 1000):
        if k % 100 == 0:
            print(f"Process {number} -- At: {k}")
        value = map.get(key)
        time.sleep(0.01)
        value.amount += 1
        map.put(key, value)

    print(f"Process {number} -- Finished! Result = {map.get(key).amount}")


if __name__ == '__main__':
    numbers = [1, 2, 3]
    procs = []

    for index, number in enumerate(numbers):
        proc = Process(target=racy_update, args=(number,))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()
