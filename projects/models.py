from django.db import models


# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=60)
    description = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=60, blank=True)

    def __str__(self):
        return self.title

    def to_string(self):
        return self.title + " " + self.description
