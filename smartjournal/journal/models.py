from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.models import User
# Create your models here.

class Journal(TimeStampedModel):
    title =  models.CharField(max_length=2000)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(default='image.png')
    file = models.FileField(default='newfile.txt')
    message = models.TextField()
    date = models.DateField()
    is_private = models.BooleanField(default=False)
    # is_therapy = models.BooleanField(default=False)
