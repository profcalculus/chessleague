from flask import current_app, g
from flask_httpauth import HTTPBasicAuth
from .errors import unauthorized

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username_or_token, password):
    from .models import User
    if current_app.config['USE_TOKEN_AUTH']:
        # token authentication
        g.user = User.verify_auth_token(username_or_token)
        return g.user is not None
    else:
        # username/password authentication
        return User.authenticate(username_or_token, password)

@auth.error_handler
def unauthorized_error():
    return unauthorized('Please authenticate to access this API')
