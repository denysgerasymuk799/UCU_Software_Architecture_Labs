def use_response_template(status, resp_msg):
    return {
        "component": "logging-service",
        "_status_code": status,
        "response": resp_msg
    }