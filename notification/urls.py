from django.urls import path
from .views import *
urlpatterns = [
    path('clients/<int:pk>/', ClientAPIView.as_view(), name='client'),
    path('clients/', ClientCreateAPIView.as_view(), name='client-create'),
    path('clients/<int:pk>/', MailAPIView.as_view(), name='mail'),
    path('mails/', MailCreateAPIView.as_view(), name='mail-create'),
    path('mails/status/', MailStatusAPIView.as_view(), name='mail-status'),
    path('mails/<int:mail_id>/messages/', MessageStatusAPIView.as_view(), name='message-status'),
    path('process-dispatches/', ProcessMailsAPIView.as_view(), name='process_dispatches'),

]
