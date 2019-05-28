from django.db import models
from account.models import User
# Create your models here.

class UserCoin(models.Model):
    Self = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'coins')
    Coin = models.IntegerField(default = 100)

    def __str__(self):
        return '%s: [%d]' % (self.Self.Nickname, self.Coin)