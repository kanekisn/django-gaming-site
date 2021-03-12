import datetime
import pytz 
from django.core.cache import cache
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from .models import *

class ActiveUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated and request.path != '/article/requests/':
            Profile.objects.update_or_create(user=request.user, defaults={'activity' : datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)})