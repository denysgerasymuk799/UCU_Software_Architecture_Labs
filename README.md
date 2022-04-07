# UCU_Software_Architecture_Labs

## Implemented Labs

✅ **Lab 1:** Microservices Basics

✅ **Lab 2:** Hazelcast Basics


## How to run the project

```shell
# Start Hazelcast management center
hz-mc start

# Start 3 nodes of Hazelcast
hz start

# Start facade-service with UI in PyCharm or with the next command
UCU_Software_Architecture_Labs/facade-service $ uvicorn facade_controller:app --workers 2 --reload --port 8081

# Start messages-service with UI in PyCharm or with the next command
UCU_Software_Architecture_Labs/messages-service $ gunicorn --bind 127.0.0.1:8083  main:app

# Start 3 instances of logging-service
UCU_Software_Architecture_Labs/logging-service $ uvicorn logging_controller:app --workers 2 --reload --port 8091
UCU_Software_Architecture_Labs/logging-service $ uvicorn logging_controller:app --workers 2 --reload --port 8092
UCU_Software_Architecture_Labs/logging-service $ uvicorn logging_controller:app --workers 2 --reload --port 8093
```
