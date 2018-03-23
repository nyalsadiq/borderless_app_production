from django.db import models


# Create your models here.
class Project(models.Model):
    owner = models.ForeignKey('auth.User',related_name='projects',on_delete=models.CASCADE)
    title = models.CharField(max_length=60)
    description = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=60, blank=True)

    def __str__(self):
        return self.title

    def to_string(self):
        return self.title + " " + self.description

class Requirement(models.Model):
    project = models.ForeignKey(Project,related_name='requirements', on_delete=models.CASCADE)
    text = models.TextField(max_length=50, blank=False)

    def __str__(self):
        return self.text
