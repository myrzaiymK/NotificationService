from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ClientSerializer
from .models import Client, Mailing, Message
from .serializers import ClientSerializer, MailingSerializer, MessageSerializer
from django.db import models
import datetime
import jwt
import requests


class ClientAPIView(APIView):
    def get_object(self, pk):
        try:
            return Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            raise ValueError('Client does not exist')

    def get(self, request, pk):
        client = self.get_object(pk)
        serializer = ClientSerializer(client)
        return Response(serializer.data)

    def put(self, request, pk):
        client = Client.objects.get(pk=pk)
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        client = self.get_object(pk)
        client.delete()
        return Response(status=204)


class ClientCreateAPIView(APIView):
    def get(self, request):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class MailCreateAPIView(APIView):
    def get(self, request):
        mails = Mailing.objects.all()
        serializer = MailingSerializer(mails, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MailingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class MailStatusAPIView(APIView):
    def get(self, request):
        mails = Mailing.objects.all()
        stats = []
        for mail in mails:
            messages_count = Message.objects.filter(mail=mail).count()
            status_counts = Message.objects.filter(mail=mail).values('status').annotate(count=models.Count('status'))
            stats.append({
                'mail_id': mail.id,
                'messages_count': messages_count,
                'status_counts': status_counts
            })
        return Response(stats)


class MailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Mail.objects.get(pk=pk)
        except Mail.DoesNotExist:
            raise ValueError('Client does not exist')

    def get(self, request, pk):
        client = self.get_object(pk)
        serializer = MailingSerializer(client)
        return Response(serializer.data)

    def put(self, request, pk):
        client = self.get_object(pk)
        serializer = MailingSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        client = self.get_object(pk)
        client.delete()
        return Response(status=204)


class MessageStatusAPIView(APIView):
    def get(self, request, mail_id):
        messages = Message.objects.filter(mail_id=mail_id)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class ProcessMailsAPIView(APIView):
    def post(self, request):
        current_time = datetime.datetime.now()
        active_mails = Mailing.objects.filter(start_time__lte=current_time, end_time__gte=current_time)

        for mail in active_mails:
            clients = Client.objects.filter(operator_code=mail.operator_code, tag=mail.tag)

            for client in clients:
                message = Message(
                    created_at=current_time,
                    status='Отправлено',
                    mail=mail,
                    client=client
                )
                try:
                    jwt_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjA0NzIxNzUsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6Imh0dHBzOi8vdC5tZS9hcndvbWFuIn0.xbTt-bL_znz5NRfQjVH_xoY4Zx3AjgbCiI8LLDjeVzA'  # Ваш JWT токен

                    headers = {'Authorization': f'Bearer {jwt_token}'}
                    payload = {'phone_number': client.phone_number, 'message_text': mail.message_text}
                    response = requests.post('https://probe.fbrq.cloud/send-message', headers=headers, json=payload)

                    if response.status_code == 200:
                        message.status = 'Доставлено'
                    else:
                        message.status = 'Не доставлено'
                except jwt.PyJWTError:
                    message.status = 'Ошибка аутентификации'
                except requests.RequestException:
                    message.status = 'Ошибка при отправке'

                message.save()

        return Response(status=200)
