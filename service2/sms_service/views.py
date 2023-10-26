import requests
from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import SMS, Room
from .tasks import send_message
from .serializers import SMSSerializer, RoomSerializer


class SMSViewSet(viewsets.ViewSet):
    serializer_class = SMSSerializer

    def create(self, request):
        token = request.COOKIES.get('access')

        if token is None:
            return Response('В доступе отказано', status=status.HTTP_400_BAD_REQUEST)

        response = requests.post('http://service1:8000/verify', json={'token': token})
        if response.status_code == 401:
            return Response('В доступе отказано', status=status.HTTP_400_BAD_REQUEST)

        try:
            good_user = request.data['receiver']
        except KeyError:
            return Response('Укажите получателя (поле "receiver")', status=status.HTTP_400_BAD_REQUEST)

        response2 = requests.get('http://service1:8000/users/' + good_user)
        good_user_id = response2.json()['id']
        bad_user_id = response.json()['id']
        response3 = requests.get('http://service1:8000/get_blist/' + str(good_user_id) + '/' + str(bad_user_id))
        if response3.status_code == 404:
            room = Room.objects.filter(receiver=request.data['receiver']).first()
            print('ROOM', room)

            try:
                content = request.data['text']
            except KeyError:
                return Response('Укажите текст сообщения (поле "text")', status=status.HTTP_400_BAD_REQUEST)

            if not room:
                room = Room(receiver=request.data['receiver'])
                room.save()

            SMS(
                content=content,
                sender_id=response.json()['id'],
                sender_name=response.json()['username'],
                room=room
            ).save()

            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)

            send_message.delay(request.data, response.json()['username'])

            return Response('Сообщение отправлено', status=status.HTTP_200_OK)
        else:
            return Response('Вы заблокированы у данного пользователя', status=status.HTTP_400_BAD_REQUEST)


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


