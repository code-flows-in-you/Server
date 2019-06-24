from django.db import models
from account.models import User
from assignment.models import Assignment
# Create your models here.

class UserCoin(models.Model):
    Self = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'coins')
    Coin = models.IntegerField(default = 100)

    def __str__(self):
        return '%s: [%d]' % (self.Self.Nickname, self.Coin)

class CoinFlow(models.Model):
    Uid = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'cf')
    Title = models.CharField(max_length = 40)
    Type = models.CharField(max_length = 40)
    TimeStamp = models.CharField(max_length = 20)
    Flow = models.IntegerField(default = 1)

    def __str__(self):
        return '[%s] %s - %s: [%d]' % (self.Type, self.Uid.Nickname, self.Title, self.Flow)