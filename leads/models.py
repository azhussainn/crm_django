from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    pass


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


class Lead(models.Model):

    SOURCE_CHOICES = (
     ('YouTube', 'YouTube'),
     ('Google', 'Google'),
     ('Facebook', 'Facebook'),
    )

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.IntegerField(default=0)
    agent = models.ForeignKey(Agent, on_delete=models.SET_DEFAULT, default=None, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

