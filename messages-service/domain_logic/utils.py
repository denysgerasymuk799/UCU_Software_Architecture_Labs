def use_response_template(status, resp_msg):
    return {
        "component": "message-service",
        "_status_code": status,
        "response": resp_msg
    }
