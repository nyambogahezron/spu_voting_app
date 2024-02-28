from base.models import User
from django.db import models

class Election(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Position(models.Model):
    title = models.CharField(max_length=200)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Voter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    has_voted = models.BooleanField(default=False)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class RunningMate(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Ballot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    running_mate = models.ForeignKey(RunningMate, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} voted for {self.running_mate.name}'