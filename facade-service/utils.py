from pydantic import BaseModel


class Message(BaseModel):
    message: str


def use_response_template(status, resp_msg):
    return {
        "_status_code": status,
        "response": resp_msg
    }
