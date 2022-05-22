from pydantic import BaseModel

from init_config import consul_client


class Message(BaseModel):
    message: str


def use_response_template(status, resp_msg):
    return {
        "_status_code": status,
        "response": resp_msg
    }


def get_all_service_urls(service_name):
    index, data = consul_client.kv.get(service_name, index=None, recurse=True)
    ip_addresses = [item['Value'].decode('utf-8') for item in data]
    print('ip_addresses -- ', ip_addresses)
