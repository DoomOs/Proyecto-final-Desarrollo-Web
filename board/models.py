from django.db import models
from django.contrib.auth.models import User


class Board(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class Project(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(User, related_name='projects', through='Member')

    def __str__(self):
        return self.name

class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.project.name}"


