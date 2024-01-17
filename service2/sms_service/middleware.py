import requests
from django.http import HttpResponse
from rest_framework import status

from service2.settings import services


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        token = request.COOKIES.get('access')

        if token is None:
            return HttpResponse('В доступе отказано', status=status.HTTP_401_UNAUTHORIZED)

        request.response = requests.post(services.service_1_verify, json={'token': token})  # ('http://' + request.host + ':8000/verify', json={'token': token})
        if request.response.status_code == 401:
            return HttpResponse('В доступе отказано', status=status.HTTP_401_UNAUTHORIZED)
