from rest_framework import serializers

from .models import Room, SMS


class SMSSerializer(serializers.ModelSerializer):
    text = serializers.CharField(max_length=1000, write_only=True, allow_blank=False)
    receiver = serializers.CharField(max_length=30, write_only=True, allow_blank=False)

    class Meta:
        model = SMS
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ['id', 'receiver']
