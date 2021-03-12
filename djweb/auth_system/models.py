from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from PIL import Image
from .storage import *
import datetime
import pytz

USER_ONLINE_TIMEOUT = 120

class Profile(models.Model):
    user     = models.OneToOneField(User, on_delete=models.CASCADE)
    img      = models.ImageField(default='profile_pics/user-1.jpg', storage=OverwriteStorage, upload_to=upload_image_path, blank=True)
    location = models.CharField(blank=True, max_length=40)
    birthdate = models.CharField(blank=True, max_length=30)
    activity = models.DateTimeField(blank=True, null=True)

    def is_online(self):
        if self.activity:
            if datetime.datetime.utcnow().replace(tzinfo=pytz.UTC) > self.activity + datetime.timedelta(seconds=USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False

    def __str__(self):
        return self.user.username
    