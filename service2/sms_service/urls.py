from django.urls import path, include
from rest_framework import routers

from .views import SMSViewSet, RoomViewSet, SMSList

router = routers.SimpleRouter()
router.register(r'sms', SMSViewSet, basename='sms')
router.register(r'sms_list', SMSList, basename='sms')
router.register(r'room', RoomViewSet, basename='room')

urlpatterns = [
    path('', include(router.urls)),
]