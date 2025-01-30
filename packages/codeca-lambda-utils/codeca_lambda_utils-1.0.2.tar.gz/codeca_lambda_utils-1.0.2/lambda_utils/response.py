import json


class LambdaResponse:
    @staticmethod
    def _format_cookies(cookies):
        """
        Format cookies as a single header string, joined by commas if multiple cookies.
        """
        formatted_cookies = [] # Checking
        for name, attributes in cookies.items():
            cookie_parts = [f"{name}={attributes['value']}"]
            if attributes.get("secure"):
                cookie_parts.append("Secure")
            if attributes.get("httpOnly"):
                cookie_parts.append("HttpOnly")
            if attributes.get("sameSite"):
                cookie_parts.append(f"SameSite={attributes['sameSite']}")
            if attributes.get("domain"):
                cookie_parts.append(f"Domain={attributes['domain']}")
            if attributes.get("maxAge"):
                cookie_parts.append(f"Max-Age={attributes['maxAge']}")
            cookie_parts.append("Path=/")  # Always include a Path
            formatted_cookies.append("; ".join(cookie_parts))
        return formatted_cookies

    @staticmethod
    def _format_headers(headers, cookies, origin):
        """
        Merge headers, cookies, and CORS headers.
        """
        response_headers = headers or {}
        multi_value_headers = {}
        if cookies:
            formatted_cookies = LambdaResponse._format_cookies(cookies)
            if len(formatted_cookies) > 1:
                multi_value_headers["Set-Cookie"] = formatted_cookies
            else:
                response_headers["Set-Cookie"] = formatted_cookies[0]
        if origin:
            response_headers["Access-Control-Allow-Origin"] = origin
            response_headers["Access-Control-Allow-Credentials"] = "true"
        return response_headers, multi_value_headers

    @staticmethod
    def _build_response(status_code, body, headers, cookies=None, origin=None):
        """
        Build a Lambda HTTP response.
        """
        response_headers, multi_value_headers = LambdaResponse._format_headers(
            headers, cookies, origin
        )
        response = {
            "statusCode": status_code,
            "headers": response_headers,
            "body": json.dumps(body),
        }
        if multi_value_headers:
            response["multiValueHeaders"] = multi_value_headers
        return response

    @staticmethod
    def success(body, status_code=200, headers=None, cookies=None, origin=None):
        """
        Return a success response.
        """
        return LambdaResponse._build_response(
            status_code, body, headers, cookies, origin
        )

    @staticmethod
    def error(message, status_code=400, headers=None, cookies=None, origin=None):
        """
        Return an error response.
        """
        return LambdaResponse._build_response(
            status_code, {"error": message}, headers, cookies, origin
        )

    @staticmethod
    def created(body, headers=None, cookies=None, origin=None):
        """
        Return a 201 Created response.
        """
        return LambdaResponse.success(
            body, status_code=201, headers=headers, cookies=cookies, origin=origin
        )

    @staticmethod
    def unauthorized(message="Unauthorized", headers=None, cookies=None, origin=None):
        """
        Return a 401 Unauthorized response.
        """
        return LambdaResponse.error(
            message, status_code=401, headers=headers, cookies=cookies, origin=origin
        )

    @staticmethod
    def forbidden(message="Forbidden", headers=None, cookies=None, origin=None):
        """
        Return a 403 Forbidden response.
        """
        return LambdaResponse.error(
            message, status_code=403, headers=headers, cookies=cookies, origin=origin
        )

    @staticmethod
    def server_error(
        message="Internal Server Error", headers=None, cookies=None, origin=None
    ):
        """
        Return a 500 Internal Server Error response.
        """
        return LambdaResponse.error(
            message, status_code=500, headers=headers, cookies=cookies, origin=origin
        )
