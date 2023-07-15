from rest_framework import serializers
from .models import Mailing, Client


class ClientSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    phone_number = serializers.CharField(max_length=11)
    operator_code = serializers.CharField(max_length=10)
    tag = serializers.CharField(max_length=255)
    timezone = serializers.CharField(max_length=50)

    def create(self, validated_data):
        return Client.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.operator_code = validated_data.get('operator_code', instance.operator_code)
        instance.tag = validated_data.get('tag', instance.tag)
        instance.timezone = validated_data.get('timezone', instance.timezone)
        instance.save()
        return instance



class MailingSerializer(serializers.ModelSerializer):
    client_filter = ClientSerializer(many=True)

    class Meta:
        model = Mailing
        fields = '__all__'


class MessageSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    status = serializers.CharField(max_length=255)
    mail_id = serializers.IntegerField()
    client_id = serializers.IntegerField()
