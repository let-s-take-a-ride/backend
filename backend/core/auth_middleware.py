import jwt
import requests
from django.http import JsonResponse

from django.conf import settings

AUTH0_DOMAIN = settings.AUTH0_DOMAIN
AUTH0_AUDIENCE = settings.AUTH0_AUDIENCE
AUTH0_JWKS = f'https://{AUTH0_DOMAIN}/.well-known/jwks.json'

class Auth0TokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        header = request.headers.get('Authorization')
        if header is None:
            return JsonResponse({'error': 'Authorization header missing'}, status=401)

        token = header.split()[1]
        resp = requests.get(f'https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json')
        jwks = resp.json()
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks['keys']:
            # print(key)
            if key['kid'] == unverified_header['kid']:
                rsa_key = {
                    'kty': key['kty'],
                    'kid': key['kid'],
                    'use': key['use'],
                    'n': key['n'],
                    'e': key['e']
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=settings.AUTH0_ALGORITHMS,
                    audience=settings.AUTH0_API_AUDIENCE,
                    issuer=f'https://{settings.AUTH0_DOMAIN}/'
                )
                return payload, True

            except Exception as e:
                JsonResponse(data={"message": "unauthorized"}, status=401)

        print("everything ok!")

        headers = {
            'Authorization': f'Bearer {token}',
        }
        url = f'https://{settings.AUTH0_DOMAIN}/userinfo'
        response = requests.get(url, headers=headers)
        user_info = response.json()
        # return user_info
        return JsonResponse(
            data={'nickname': user_info.get('nickname', 'N/A'), 'picture': user_info.get('picture', 'N/A')}, status=200)
