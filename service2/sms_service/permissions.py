import requests
from rest_framework.permissions import BasePermission


class MyAuthenticated(BasePermission):

    def has_permission(self, request, view):
        token = request.COOKIES.get('access')

        if token is None:
            return False

        response = requests.post('http://127.0.0.1:8000/verify', json={'token': token})
        if response.status_code == 200:
            return True
        else:
            return False
