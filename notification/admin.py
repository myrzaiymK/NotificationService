from django.contrib import admin
from .models import Client, Message, Mailing

# Register your models here.

admin.site.register(Client)
admin.site.register(Message)
admin.site.register(Mailing)

