from django.db import models


# Create your models here.
class Image(models.Model):
    image = models.ImageField(upload_to="images/")

class Video(models.Model):
    video = models.FileField(upload_to="videos/")