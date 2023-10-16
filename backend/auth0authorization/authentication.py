import requests
from django.conf import settings
from django.contrib.auth import get_user_model
import jwt
from rest_framework import exceptions
from rest_framework.authentication import (BaseAuthentication,
                                           get_authorization_header)

import json
User = get_user_model()
print("in auth")

def is_valid_auth0token(token):
    # TODO: remove request and make the `json` file as part of the project to save the request time
    jwks_url = f'https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json'
    jwks = requests.get(jwks_url).json()

    public_key = None
    header_kid = jwt.get_unverified_header(token).get('kid')
    for jwk in jwks['keys']:
        if jwk['kid'] == header_kid:
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))
            break

    try:
        payload = jwt.decode(
            token,
            public_key,
            audience=settings.AUTH0_AUDIENCE,
            issuer=f'https://{settings.AUTH0_DOMAIN}/',
            algorithms=['RS256']
        )
        return payload, True
    except jwt.ExpiredSignatureError:
        print("error")
        raise exceptions.AuthenticationFailed('token is expired')
    except jwt.JWTClaimsError:
        print("error")
        raise exceptions.AuthenticationFailed(
            'incorrect claims, please check the audience and issuer'
        )
    except Exception as e:
        print("error")
        raise exceptions.AuthenticationFailed(
            'Unable to parse authentication'
        )
    return {}, False


def get_auth0_user_data(token, sub):
    url = f'https://{settings.AUTH0_DOMAIN}/api/v2/users/{sub}'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    # print(token)
    resp = requests.get(url, headers=headers)
    data = resp.json()
    print(data)
    return data

class Auth0TokenAuthentication(BaseAuthentication):
    keyword = 'Bearer'
    err_msg = 'Invalid token headers'

    def authenticate(self, request):
        print("in authenticate")
        header = request.headers.get('Authorization')
        if header is None:
            raise exceptions.AuthenticationFailed(self.err_msg)

        token = header.split()[1]
        return self.authenticate_credentials(token)

    def authenticate_credentials(self, token):
        global user
        print("auth_credentials")
        payload, is_valid = is_valid_auth0token(token)
        print(is_valid)
        if not is_valid:
            raise exceptions.AuthenticationFailed(self.err_msg)

        # print(payload)
        auth0_username = payload['sub']
        print(auth0_username)
        # breakpoint()
        user_data = get_auth0_user_data(token, auth0_username)
        nick = user_data.get('nickname')
        print(nick)
        picture = user_data.get('picture')
        email = user_data.get('email')

        if not email:
            raise exceptions.AuthenticationFailed(self.err_msg)


        user = User.objects.filter(email=email).last()
        if user is None:
            user = User.objects.create(email=email, nickname=nick, picture=picture)
            user.save()
        print(user)
        return user, token