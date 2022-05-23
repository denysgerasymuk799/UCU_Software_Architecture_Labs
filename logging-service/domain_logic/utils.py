def use_response_template(status, resp_msg):
    return {
        "component": "logging_service",
        "_status_code": status,
        "response": resp_msg
    }


def get_consul_kv_value(consul_client, key):
    index, data = consul_client.kv.get(key, index=None)
    if data:
        return data['Value'].decode('utf-8')
    return None


def get_all_service_urls(consul_client, service_name):
    index, data = consul_client.kv.get(service_name, index=None, recurse=True)
    ip_addresses = [item['Value'].decode('utf-8') for item in data]
    return ip_addresses
