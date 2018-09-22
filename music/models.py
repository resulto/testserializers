from django.db import models

# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=250)


class Album(models.Model):
    name = models.CharField(max_length=250)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    code = models.CharField(max_length=18, unique=True)


class Track(models.Model):
    song = models.CharField(max_length=250)
    album = models.ForeignKey(
        Album, on_delete=models.CASCADE, related_name="tracks")
    index = models.IntegerField()

    class Meta:
        unique_together = [
            ("album", "index")
        ]
