from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entry_xml = models.TextField()
    entry_link = models.CharField(max_length=1000, default="")
