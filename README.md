# UCU_Software_Architecture_Labs

## Implemented Labs

✅ **Lab 1:** Microservices Basics

✅ **Lab 2:** Hazelcast Basics

✅ **Lab 3:** Microservices with Hazelcast

**Lab 4:** Microservices with Messaging queue


## How to run the project

```shell
# Start 3 nodes of Hazelcast
hz start

# Start Hazelcast management center
hz-mc start

# Start facade-service with UI in PyCharm or with the next command
UCU_Software_Architecture_Labs/facade-service $ uvicorn facade_controller:app --workers 2 --reload --port 8081

# Start 2 instances of messages-service with the next commands or use messages_service/start_service.sh
UCU_Software_Architecture_Labs/messages-service $ gunicorn --bind 127.0.0.1:8083  message_controller:app
UCU_Software_Architecture_Labs/messages-service $ gunicorn --bind 127.0.0.1:8084  message_controller:app

# Start 3 instances of logging-service with the next commands or use logging_service/start_service.sh
UCU_Software_Architecture_Labs/logging-service $ uvicorn logging_controller:app --workers 2 --reload --port 8091
UCU_Software_Architecture_Labs/logging-service $ uvicorn logging_controller:app --workers 2 --reload --port 8092
UCU_Software_Architecture_Labs/logging-service $ uvicorn logging_controller:app --workers 2 --reload --port 8093
```
