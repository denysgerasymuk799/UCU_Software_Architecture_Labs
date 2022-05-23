from pydantic import BaseModel
from pprint import pprint


class Message(BaseModel):
    message: str


def use_response_template(status, resp_msg):
    return {
        "_status_code": status,
        "response": resp_msg
    }


def get_consul_kv_value(consul_client, key):
    index, data = consul_client.kv.get(key, index=None)
    if data:
        return data['Value'].decode('utf-8')
    return None


def get_all_service_urls(consul_client, service_name):
    index, data = consul_client.catalog.service(service_name)
    print(f'{service_name}/api_root_path')
    api_root_path = get_consul_kv_value(consul_client, key=f'{service_name}/api_root_path')
    print('api_root_path -- ', api_root_path)
    pprint(data)
    if api_root_path:
        ip_addresses = [f"http://{item['ServiceAddress']}:{int(item['ServicePort'])}{api_root_path}" for item in data]
    else:
        ip_addresses = [f"http://{item['ServiceAddress']}:{int(item['ServicePort'])}" for item in data]
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
