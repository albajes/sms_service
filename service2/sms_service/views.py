import requests
from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import SMS, Room
from .tasks import send_message
from .serializers import SMSSerializer, RoomSerializer
from service2.settings import services


class SMSViewSet(viewsets.ViewSet):
    serializer_class = SMSSerializer

    def create(self, request):

        try:
            good_user = request.data['receiver']
        except KeyError:
            return Response('Укажите получателя (поле "receiver")', status=status.HTTP_400_BAD_REQUEST)

        response2 = requests.get(services.service_1_users + good_user)  # ('http://' + request.host + ':8000/users/' + good_user)
        good_user_id = response2.json()['id']
        bad_user_id = request.response.json()['id']
        response3 = requests.get(services.service_1_blist + str(good_user_id) + '/' + str(bad_user_id))  # ('http://' + request.host + ':8000/get_blist/'
                                                                                                         # + str(good_user_id) + '/'
                                                                                                         # + str(bad_user_id))

        if response3.status_code == 200:
            return Response('Вы заблокированы у данного пользователя', status=status.HTTP_400_BAD_REQUEST)

        room = Room.objects.filter(receiver=request.data['receiver']).first()

        try:
            content = request.data['text']
        except KeyError:
            return Response('Укажите текст сообщения (поле "text")', status=status.HTTP_400_BAD_REQUEST)

        if not room:
            room = Room(receiver=request.data['receiver'])
            room.save()

        SMS(
            content=content,
            sender_id=request.response.json()['id'],
            sender_name=request.response.json()['username'],
            room=room
        ).save()

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        send_message.delay(request.data, request.response.json()['username'])

        return Response('Сообщение отправлено', status=status.HTTP_200_OK)


class SMSList(viewsets.ViewSet):

    def list(self, request):
        queryset = SMS.objects.all()
        serializer = SMSSerializer(queryset, many=True)
        return Response(serializer.data)


class RoomViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Room.objects.all()
        serializer = RoomSerializer(queryset, many=True)
        return Response(serializer.data)


