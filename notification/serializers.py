from rest_framework import serializers
from .models import Mailing

# class MailingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Mailing
#         fields = ['id', 'start_time', 'end_time', 'message_text', 'client_filter']
#
# class ClientSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Client
#         fields = ['id', 'phone_number', 'operator_code', 'tag', 'timezone']

class MailingSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    message_text = serializers.CharField(max_length=255)
    client_filter = serializers.ListField(child=serializers.CharField(max_length=255))

class ClientSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    phone_number = serializers.CharField(max_length=11)
    operator_code = serializers.CharField(max_length=10)
    tag = serializers.CharField(max_length=255)
    timezone = serializers.CharField(max_length=50)
