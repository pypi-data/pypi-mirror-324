import datetime
import hmac
import hashlib
import base64
import requests
import json

from urllib.parse import urlunsplit, urlencode


class InterfolioBase:
    def __init__(self, config):
        self.config = config

    def _build_and_send_request(self, api_endpoint, api_method, payload=None, data=None, files=None, **query_params):
        api_url = self._build_api_url(api_endpoint, **query_params)
        headers = self._build_headers(api_endpoint, api_method, **query_params)
        
        try:
            if api_method == "POST":
                response = requests.post(api_url, headers=headers, json=payload, data=data, files=files)
            elif api_method == "GET":
                response = requests.get(api_url, headers=headers)
            elif api_method == "DELETE":
                response = requests.delete(api_url, headers=headers)
            else:
                raise ValueError("Unsupported HTTP method.")
            
            response.raise_for_status()
            return response.json() if response.content else {}
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

    @staticmethod
    def _make_get_request(api_url, headers):
        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            return json.loads(response.text)
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

    @staticmethod
    def _make_delete_request(api_url, headers):
        try:
            response = requests.delete(api_url, headers=headers)
            response.raise_for_status()
            return
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

    @staticmethod
    def _make_post_request(api_url, headers, payload):
        print("posting")
        try:
            response = requests.post(api_url, headers=headers, json=payload)
            print("------------")
            print("url: ", response.request.url)
            print("body: ", response.request.body)
            print("headers: ", response.request.headers)
            print("json: ", payload)
            print("------------")
            print(api_url, headers, payload)
            response.raise_for_status()
            return json.loads(response.text)
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

    def _build_api_url(self, api_endpoint, **query_params):
        query = urlencode(query_params)
        url = urlunsplit(("https", self.config.host, api_endpoint, query, ""))
        return url

    def _build_headers(self, api_endpoint, api_method, **query_params):
        timestamp = self._create_timestamp()
        message = self._build_message(
            api_endpoint, api_method, timestamp, **query_params
        )
        signature = self._build_signature(message)
        header = {
            "TimeStamp": self._create_timestamp(),
            "Authorization": self._build_authentication_header(signature),
        }
        if hasattr(self.config, "database_id"):
            header["INTF-DatabaseID"] = self.config.database_id
        return header

    @staticmethod
    def _create_timestamp():
        return datetime.datetime.now(datetime.timezone.utc).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    @staticmethod
    def _build_message(api_endpoint, api_method, timestamp, **query_params):
        return f"{api_method}\n\n\n{timestamp}\n{api_endpoint}"

    def _build_signature(self, message):
        signature_bytes = hmac.new(
            self.config.private_key.encode(), message.encode(), hashlib.sha1
        ).digest()
        return base64.b64encode(signature_bytes).decode()

    def _build_authentication_header(self, signature):
        return f"INTF {self.config.public_key}:{signature}"

    def _get_raw_document(self, api_endpoint, api_method, **query_params):
        """
        Make a GET request and return the raw response without JSON parsing
        """
        api_url = self._build_api_url(api_endpoint, **query_params)
        headers = self._build_headers(api_endpoint, api_method, **query_params)
        
        try:
            print("Making GET request to:", api_url)  # Debug
            print("With headers:", headers)           # Debug
            response = requests.get(api_url, headers=headers)
            print("Response status:", response.status_code)  # Debug
            print("Response headers:", response.headers)     # Debug
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
