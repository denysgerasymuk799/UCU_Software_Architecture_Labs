# ======================== Microservices configs ========================
host_ip="127.0.0.1"

consul kv put facade_service/host_ip ${host_ip}
consul kv put logging_service/host_ip ${host_ip}
consul kv put messages_service/host_ip ${host_ip}

consul kv put logging_service/get_msgs_endpoint '/get_messages'
consul kv put logging_service/add_msg_endpoint '/add_message'

consul kv put messages_service/get_msgs_endpoint '/get_messages'
consul kv put messages_service/add_msg_endpoint '/add_message'


# ======================== Hazelcast configs ========================
hz_dir="hazelcast/"
consul kv delete -recurse "${hz_dir}hz_node_"

uuid1=$(uuidgen)
hazelcast_name1="${hz_dir}hz_node_${uuid1}"
consul kv put ${hazelcast_name1} "${host_ip}:5701"

uuid2=$(uuidgen)
hazelcast_name2="${hz_dir}hz_node_${uuid2}"
consul kv put ${hazelcast_name2} "${host_ip}:5702"

uuid3=$(uuidgen)
hazelcast_name3="${hz_dir}hz_node_${uuid3}"
consul kv put ${hazelcast_name3} "${host_ip}:5703"

consul kv put hazelcast/hz_distributed_map 'lab3_distributed_map1'


# ======================== Kafka configs ========================
consul kv delete -recurse 'kafka/kafka_broker_1'

kafka_broker_name1="kafka/kafka_broker_1"
consul kv put ${kafka_broker_name1} "${host_ip}:9092"

consul kv put kafka/messages_svc_topic 'MessageSvcTopic'
consul kv put kafka/consumer_group 'MessageSvcConsumerGroup'
