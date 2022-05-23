def use_response_template(status, resp_msg):
    return {
        "component": "message-service",
        "_status_code": status,
        "response": resp_msg
    }


def get_consul_kv_value(consul_client, key):
    return consul_client.kv.get(key)['Value'].decode('utf-8')


def get_all_service_urls(consul_client, service_name):
    index, data = consul_client.kv.get(service_name, index=None, recurse=True)
    ip_addresses = [item['Value'].decode('utf-8') for item in data]
    return ip_addresses


def add_service_to_consul(consul_client, service_name, service_key, service_address):
    index, data = consul_client.kv.get(service_name, index=None, recurse=True)
    unique_addresses = set()
    if data:
        for item in data:
            addr = item['Value'].decode('utf-8')
            unique_addresses.add(addr)

    if service_address not in unique_addresses:
        consul_client.kv.put(key=service_key, value=service_address)
