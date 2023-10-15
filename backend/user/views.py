from django.http import JsonResponse
from django.views import View

class TestAuthenticationView(View):

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'Hello!'})
