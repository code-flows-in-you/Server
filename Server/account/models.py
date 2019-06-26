from django.db import models
from system.storage import ImageStorage

# Create your models here.

class User(models.Model):
    # required
    UserID = models.AutoField(primary_key = True)
    Email = models.CharField(max_length = 30)
    Password = models.CharField(max_length = 20)
    # 不实现 类别: 学生/组织 
    # Class = models.IntegerField(default = 0)
    Nickname = models.CharField(max_length = 20)
    Gender = models.CharField(max_length = 10, default = 'male')

    # not required
    Avatar = models.ImageField(upload_to = 'avatar', storage = ImageStorage(), default = 'avatar/default.jpg') 
    Grade = models.CharField(max_length = 4, default = '2018')
    College = models.CharField(max_length = 30, default = '未填写')
    Major = models.CharField(max_length = 20, default = '未填写')
    StudentID = models.IntegerField(default = 0)
    RealName = models.CharField(max_length = 12, default = '未填写')

    def __str__(self):
        return '%d: [%s][%s]' % (self.UserID, self.Email, self.Nickname)