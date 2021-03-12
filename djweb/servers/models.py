from django.db import models

class Servers(models.Model):
    ip = models.CharField(max_length=200, null=False)
    port = models.IntegerField(null=False)
    password = models.CharField(max_length=200, null=False)

    def __str__(self):
        return f'{self.ip}:{self.port}'