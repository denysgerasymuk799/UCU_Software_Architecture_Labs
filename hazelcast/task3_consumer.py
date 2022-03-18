import hazelcast
import threading

client = hazelcast.HazelcastClient()
queue = client.get_queue("queue")


def consume():
    consumed_count = 0
    while consumed_count < 100:
        head = queue.take().result()
        print("Consuming {}".format(head))
        consumed_count += 1


if __name__ == '__main__':
    consumer_thread = threading.Thread(target=consume)
    consumer_thread.start()
    consumer_thread.join()

    client.shutdown()
