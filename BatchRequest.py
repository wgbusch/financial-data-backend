import json
import uuid

import requests


def fun_parse(result):
    return json.loads(result[result.find('{'):].strip())


class BatchRequest:
    'Class for sending several HTTP requests in a single request'

    def __init__(self, token):
        self.batch_url = 'https://gateway.saxobank.com/sim/openapi/ref/batch'
        self.boundary = "batch_" + str(uuid.uuid4())
        self.data = ""
        self.headers = {"Content-Type": "multipart/mixed; boundary=\"{0}\"".format(self.boundary),
                        "Authorization": "Bearer " + token}
        self.host = "gateway.saxobank.com"

    # Build sub-request depending on Method and Data supplied
    def add_request(self, method, url, data={}):
        boundary = self.boundary
        host = self.host

        if method == "GET":
            self.data += "--{0}\r\nContent-Type: application/http; msgtype=request\r\n\r\n{1} {2} HTTP/1.1\r\nHost: {3}\r\n\r\n\r\n".format(
                boundary, method, url, host)

        # If no data, have alternative option
        elif method == "POST" or method == "PUT":
            self.data += "--{0}\r\nContent-Type: application/http; msgtype=request\r\n{1} {2} HTTP/1.1\r\nHost: {3}\r\nContent-Type: application/json; charset=utf-8\r\n\r\n{3}\r\n".format(
                boundary, method, url, json.dumps(data), host)

        elif method == "DELETE":
            self.data += "--{0}\r\nContent-Type: application/http; msgtype=request\r\n{1} {2} HTTP/1.1\r\nHost: {3}\r\n\r\n\r\n".format(
                boundary, method, url, host)

    def execute_request(self):
        # Add the "closing" boundary
        self.data += "--{0}--".format(self.boundary)

        response = requests.post(self.batch_url, data=self.data, headers=self.headers)

        content_type = response.headers['Content-Type']
        start_boundary = response.headers['Content-Type'].find("boundary=\"")
        boundary = content_type[start_boundary + 10:start_boundary + 10 + len(str(uuid.uuid4()))]

        results = response.text.split("--" + boundary)[1:-1]
        results = list(map(lambda result: fun_parse(result), results))
        return results
