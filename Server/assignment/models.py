from django.db import models
from account.models import User
# Create your models here.

class Assignment(models.Model):
    Aid = models.AutoField(primary_key = True)
    Title = models.CharField(max_length = 40)
    Description = models.CharField(max_length = 100)
    Type = models.CharField(max_length = 20)
    Creator = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'asg')
    Coins = models.IntegerField(default = 1)
    CreateTime = models.CharField(max_length = 20)
    StartTime = models.CharField(max_length = 20)
    EndTime = models.CharField(max_length = 20)

    def __str__(self):
        return '%d: [%s] [%s]' % (self.Aid, self.Title, self.Description)