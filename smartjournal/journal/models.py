from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.models import User

from smartjournal import settings
# Create your models here.

class Journal(TimeStampedModel):
    title =  models.CharField(max_length=2000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image = models.ImageField(null=True, blank=True)
    files = models.FileField(null=True, blank=True)
    audio_file = models.FileField(default=None, null=True, blank=True)
    message = models.TextField(blank=True)
    date = models.DateField()
    is_private = models.BooleanField(default=False)
    data = models.TextField(default=None, null=True)

    # is_therapy = models.BooleanField(default=False)
