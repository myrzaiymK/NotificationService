from django.db import models

# Create your models here.


class Mailing(models.Model):
    id = models.AutoField(primary_key=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    message_text = models.TextField()
    client_filter = models.ManyToManyField('Client', related_name='mails')

    def __str__(self):
        return f"Mailing {self.id}"


class Client(models.Model):
    id = models.AutoField(primary_key=True)
    phone_number = models.CharField(max_length=11)
    operator_code = models.CharField(max_length=10)
    tag = models.CharField(max_length=255)
    timezone = models.CharField(max_length=50)

    def __str__(self):
        return f"Client {self.id}"


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    dispatch = models.ForeignKey('Mailing', on_delete=models.CASCADE)
    client = models.ForeignKey('Client', on_delete=models.CASCADE)

    def __str__(self):
        return f"Message {self.id}"
