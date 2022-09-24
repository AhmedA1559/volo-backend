# Flask middleware for verifying Google ID tokens passed in the Authorization HTTP header.
#
# This module provides a middleware class that can be used to verify ID tokens passed in the
# Authorization HTTP header. The middleware will parse the ID token, verify its signature and
# validity, and then set the current user to the decoded token. The middleware will also reject
# requests with invalid tokens.
from firebase_admin import auth
from functools import wraps

from flask import request, jsonify, make_response


def auth_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        """Decorator that verifies the signature and data for the provided JWT.
        Accepts either an unsigned or signed JWT string. Returns a dictionary with the token claims if
        the signature is valid. Otherwise, returns None.
        Args:
            id_token: A string of the encoded JWT.
            app: An App instance (optional).
        Returns:
            dict: A dictionary of key-value pairs parsed from the decoded JWT.
            None: If the JWT failed to verify.
        """
        id_token = request.headers.get('Authorization').split(' ').pop()
        if not id_token:
            return make_response(jsonify({'error': 'Authorization header is missing'}), 401)

        try:
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token['uid']

            return f(uid, *args, **kwargs)
        except Exception as e:
            return make_response(jsonify({'error': e}), 401)
    return decorator
