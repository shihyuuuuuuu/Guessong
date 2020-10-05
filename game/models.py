from django.db import models

# Create your models here.
class Song(models.Model):
    sid = models.IntegerField()
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    singer = models.CharField(max_length=100, default="unknown singer")
    seconds = models.IntegerField()
    views = models.IntegerField()
    audio = models.FileField()
    url = models.URLField()

    def __str__(self):
        """String for representing the Model object."""
        return self.title