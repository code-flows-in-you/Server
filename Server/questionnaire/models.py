from django.db import models
from assignment.models import Assignment
from account.models import User

# Create your models here.

class Questions(models.Model):
    Qid = models.AutoField(primary_key = True)
    Aid = models.ForeignKey(Assignment, on_delete = models.CASCADE, related_name = 'qnn')
    Title = models.CharField(max_length = 40)
    Type = models.CharField(max_length = 20)

    def __str__(self):
        return '%d: [%s] [%s]' % (self.Qid, self.Title, self.Type)

class Options(models.Model):
    Oid = models.AutoField(primary_key = True)
    Qid = models.ForeignKey(Questions, on_delete = models.CASCADE, related_name = 'opt')
    Aid = models.ForeignKey(Assignment, on_delete = models.CASCADE, related_name = 'opt')
    Value = models.CharField(max_length = 40)

    def __str__(self):
        return '%d: [%s]' % (self.Oid, self.Value)

class Answer(models.Model):
    ASid = models.AutoField(primary_key = True)
    Oid = models.ForeignKey(Options, on_delete = models.CASCADE, related_name = 'ans')
    Qid = models.ForeignKey(Questions, on_delete = models.CASCADE, related_name = 'ans')
    Aid = models.ForeignKey(Assignment, on_delete = models.CASCADE, related_name = 'ans')
    Uid = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'ans')
    Value = models.CharField(max_length = 40)
    TimeStamp = models.CharField(max_length = 30)

    def __str__(self):
        return '%d: [%s] [%s]' % (self.ASid, self.Uid.Nickname, self.Value)

class QnnCoin(models.Model):
    QCid = models.AutoField(primary_key = True)
    Aid = models.ForeignKey(Assignment, on_delete = models.CASCADE, related_name = 'qnncoin')
    Coin = models.IntegerField(default = 1)
    Copy = models.IntegerField(default = 1)

    def __str__(self):
        return '%d: [%s] [%d*%d]' % (self.QCid, self.Aid.Title, self.Coin, self.Copy)