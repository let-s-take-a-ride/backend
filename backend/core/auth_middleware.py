import jwt
import requests
from django.http import JsonResponse
import json
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

        token = header.split()[1]  # Assuming header is in the format "Bearer <token>"
        jwks_url = f'https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json'
        jwks = requests.get(jwks_url).json()

        public_key = None
        header_kid = jwt.get_unverified_header(token).get('kid')
        for jwk in jwks['keys']:
            if jwk['kid'] == header_kid:
                public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))
                break

        if public_key is None:
            return JsonResponse({'error': 'Public key not found'}, status=401)

        try:
            payload = jwt.decode(
                token,
                public_key,
                audience=settings.AUTH0_AUDIENCE,
                issuer=f'https://{settings.AUTH0_DOMAIN}/',
                algorithms=['RS256']
            )
            print(payload)
        except jwt.InvalidTokenError as e:
            return JsonResponse({'error': str(e)}, status=401)

        request.token_payload = payload

        response = self.get_response(request)
        return response
