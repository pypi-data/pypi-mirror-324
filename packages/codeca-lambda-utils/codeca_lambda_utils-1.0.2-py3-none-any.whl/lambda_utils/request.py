# shared/lambda_utils/request.py
import json

import jwt


class LambdaRequest:
    def __init__(self, event):
        """
        Initialize the request object with a raw Lambda event.
        """
        self.event = event
        self.body = self._parse_body()
        self.query_params = event.get("queryStringParameters", {}) or {}
        self.path_params = event.get("pathParameters", {}) or {}
        self.headers = event.get("headers", {}) or {}
        self.cookies = self._parse_cookies()

    def _parse_body(self):
        """
        Parse the body of the request (assumes JSON payloads).
        """
        if self.event.get("body"):
            try:
                return json.loads(self.event["body"])
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON format in request body")
        return {}

    def _parse_cookies(self):
        """
        Parse cookies from the headers.
        """
        cookie_header = self.headers.get("cookie", "") # Used to be Cookie
        cookies = {}
        if cookie_header:
            for cookie in cookie_header.split(";"):
                if "=" in cookie:
                    key, value = cookie.strip().split("=", 1)
                    cookies[key] = value
        return cookies

    def get_body(self):
        return self.body

    def get_body_param(self, key, default=None):
        """
        Retrieve a parameter from the request body.
        """
        return self.body.get(key, default)

    def get_query_param(self, key, default=None):
        """
        Retrieve a query string parameter.
        """
        return self.query_params.get(key, default)

    def get_path_param(self, key, default=None):
        """
        Retrieve a path parameter.
        """
        return self.path_params.get(key, default)

    def get_cookie(self, key, default=None):
        """
        Retrieve a cookie by name.
        """
        return self.cookies.get(key, default)

    @property
    def records(self):
        """
        Return the records (if present) from the event, e.g., SQS or DynamoDB streams.
        """
        return self.event.get("Records", [])

    @staticmethod
    def _decode_jwt(token):
        """
        Decode the JWT token to extract claims.
        """
        try:
            # Decode without verifying the signature (for extracting claims only)
            return jwt.decode(token, options={"verify_signature": False})
        except jwt.PyJWTError as e:
            raise ValueError(f"Invalid JWT token: {e}")

    def get_authorizer_attribute(self, key):
        """
        Retrieve a custom attribute from the `requestContext.authorizer` in the event.
        :param key: The key to retrieve (e.g., 'organizationId', 'email').
        :return: The value of the attribute, or None if not found.
        """
        authorizer_context = self.event.get("requestContext", {}).get("authorizer", {})
        print(authorizer_context)
        return authorizer_context.get(key)
