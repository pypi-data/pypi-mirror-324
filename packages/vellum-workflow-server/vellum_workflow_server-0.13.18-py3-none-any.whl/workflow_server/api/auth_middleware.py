import json

from flask import Request, Response
import jwt
from jwt import ExpiredSignatureError

from workflow_server.config import VEMBDA_PUBLIC_KEY, is_development


class AuthMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        try:
            request = Request(environ)
            if not request.path.startswith("/healthz") and not is_development():
                token = request.headers.get("X-Vembda-Signature")
                jwt.decode(token, VEMBDA_PUBLIC_KEY, algorithms=["RS256"])

        except ExpiredSignatureError:
            res = Response(
                json.dumps({"detail": "Signature token has expired. Please obtain a new token."}),
                mimetype="application/json",
                status=401,
            )
            return res(environ, start_response)
        except Exception as e:
            res = Response(
                json.dumps({"detail": f"Invalid signature token {str(e)}"}), mimetype="application/json", status=401
            )
            return res(environ, start_response)

        return self.app(environ, start_response)
