from django.db import models
from model_utils.models import TimeStampedModel
from django.contrib.auth.models import User
# Create your models here.

class Journal(TimeStampedModel):
    title =  models.TextField()
    user = models.ForeignKey(User)

    message = models.TextField()
    date = models.DateTimeField()
    is_private = models.BooleanField(default=False)
    # is_therapy = models.BooleanField(default=False)
