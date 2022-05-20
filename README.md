# UCU_Software_Architecture_Labs

## Implemented Labs

✅ **Lab 1:** Microservices Basics

✅ **Lab 2:** Hazelcast Basics

✅ **Lab 3:** Microservices with Hazelcast

✅ **Lab 4:** Microservices with Messaging queue


## Configurations

```shell
# Start 3 nodes of Hazelcast
hz start

# Start Hazelcast management center
hz-mc start

# Download kafka zip locally from https://kafka.apache.org/downloads
# and enter its bin directory

# Start zookeeper server
zookeeper-server-start.sh config/zookeeper.properties

# Start kafka bootstrap server
kafka-server-start.sh config/server.properties

# Create Kafka topics
kafka-topics --zookeeper 127.0.0.1:2181  --topic MessageSvcTopic --create --partitions 3 --replication-factor 1

# Example how to read messages from topics with Kafka consumer CLI
kafka-console-consumer --bootstrap-server 127.0.0.1:9092 --topic MessageSvcTopic --from-beginning
```


## How to run the project

```shell
# Start facade-service with UI in PyCharm or with the next command
UCU_Software_Architecture_Labs/facade-service $ uvicorn facade_controller:app --workers 2 --reload --port 8081

# Start 2 instances of messages-service with the next commands or 
# use the next command -- bash messages_service/start_service.sh <PORT_NUM>
UCU_Software_Architecture_Labs/messages-service $ gunicorn --bind 127.0.0.1:8083  message_controller:app
UCU_Software_Architecture_Labs/messages-service $ gunicorn --bind 127.0.0.1:8084  message_controller:app

# Start 3 instances of logging-service with the next commands or 
# use the next command -- bash logging_service/start_service.sh <PORT_NUM>
UCU_Software_Architecture_Labs/logging-service $ uvicorn logging_controller:app --workers 2 --reload --port 8091
UCU_Software_Architecture_Labs/logging-service $ uvicorn logging_controller:app --workers 2 --reload --port 8092
UCU_Software_Architecture_Labs/logging-service $ uvicorn logging_controller:app --workers 2 --reload --port 8093
```
