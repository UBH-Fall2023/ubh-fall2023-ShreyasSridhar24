from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.models import User
# Create your models here.

class Journal(TimeStampedModel):
    title =  models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    message = models.TextField()
    date = models.DateTimeField()
    is_private = models.BooleanField(default=False)
    # is_therapy = models.BooleanField(default=False)
