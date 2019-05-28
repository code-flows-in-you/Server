from django.db import models
from account.models import User
from assignment.models import Assignment
# Create your models here.

class Problem(models.Model):
    Pid = models.AutoField(primary_key = True)
    Aid = models.ForeignKey(Assignment, on_delete = models.CASCADE, related_name = 'pro')
    Detail = models.CharField(max_length = 100)

    def __str__(self):
        return '%d: [%s]' % (self.Pid, self.Detail)

class Answer(models.Model):
    QAid = models.AutoField(primary_key = True)
    Aid = models.ForeignKey(Assignment, on_delete = models.CASCADE, related_name = 'qas')
    Pid = models.ForeignKey(Problem, on_delete = models.CASCADE, related_name = 'qas')
    Uid = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'qas')
    Value = models.CharField(max_length = 200)
    TimeStamp = models.CharField(max_length = 30)

    def __str__(self):
        return '%d: [%s] [%s]' % (self.QAid, self.Uid.Nickname, self.Value)

class Best(models.Model):
    Bid = models.AutoField(primary_key = True)
    Aid = models.ForeignKey(Assignment, on_delete = models.CASCADE, related_name = 'qab')
    Pid = models.ForeignKey(Problem, on_delete = models.CASCADE, related_name = 'qab')
    Uid = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'qab')
    Value = models.CharField(max_length = 200)
    TimeStamp = models.CharField(max_length = 30)

    def __str__(self):
        return '%d: [%s] [%s]' % (self.Bid, self.Uid.Nickname, self.Value)
