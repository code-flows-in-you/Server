from django.forms.models import model_to_dict
from django.http import HttpResponse
import json
from .models import User
from coin.models import UserCoin

# Create your views here.

def okMSG(jsonObj = {}):
    return HttpResponse(json.dumps(jsonObj), content_type = 'application/json') 

def failMSG(msg = ''):
    response = {'msg': msg}
    return HttpResponse(json.dumps(response), status=400, content_type = 'application/json') 

def register(request):
    # 检查登录状态
    if 'login_id' in request.session:
        return failMSG('already login')
    
    # 检查 method
    if request.method != 'POST':
        return failMSG('wrong method')
        
    # 获取参数
    try:
        t_email = request.POST['email']
        t_password = request.POST['password']
        # t_class = request.POST['class']
        t_gender = request.POST['gender']
        t_nickname = request.POST['nickname']
    except Exception as e:
        return failMSG('POST parameter error')
    
    if t_gender != 'male' or t_gender != 'female':
        t_gender = 'male'

    # 数据库操作
    try:
        t_user = User.objects.filter(Email = t_email)
    except Exception as e:
        return failMSG('db error')
    else:
        if t_user.count() == 0:
            temp = User.objects.create(
                Email = t_email,
                Password = t_password,
                # Class = t_class,
                Gender = t_gender,
                Nickname = t_nickname
            )
            t_ucoin = UserCoin.objects.create(
                Self = temp
            )
            return okMSG({'msg':'register successfully', 'uid':temp.UserID})
        else:
            return failMSG('repeat email')

    return failMSG('fail')

def session(request):

    # 登出
    if request.method == 'DELETE':
        try:
            del request.session['login_id']
        except KeyError:
            return failMSG('no login')

        return okMSG({'msg':'logout successfully'})

    # 下面只接受 POST
    if request.method != 'POST':
        return failMSG('wrong method')
        
    # 获取参数
    try:
        t_email = request.POST['email']
        t_password = request.POST['password']
    except Exception as e:
        return failMSG('POST parameter error')
        
    # 数据库操作
    try:
        t_user = User.objects.filter(Email = t_email, Password = t_password)
    except Exception as e:
        return failMSG('db error')
    else:
        if t_user.count() <= 0:
            return failMSG('email or password error')
        else:
            request.session['login_id'] = t_user[0].UserID
            return okMSG({'uid':t_user[0].UserID})

    return failMSG('fail')

def getInfo(request, t_uid):

    # 下面只接受 GET
    if request.method != 'GET':
        return failMSG('wrong method')

    # 数据库操作
    try:
        t_user = User.objects.filter(UserID = t_uid)
    except Exception as e:
        return failMSG('db error')
    else:
        if t_user.count() == 1:
            t_user = t_user[0]
            temp = {}
            temp['UserID'] = t_user.UserID
            temp['Email'] = t_user.Email
            # temp['Class'] = t_user.Class
            temp['Gender'] = t_user.Gender
            temp['Nickname'] = t_user.Nickname
            temp['Avatar'] = t_user.Avatar.url
            temp['Description'] = t_user.Description
            temp['Grade'] = t_user.Grade
            temp['College'] = t_user.College
            temp['Major'] = t_user.Major
            temp['StudentID'] = t_user.StudentID
            temp['RealName'] = t_user.RealName
            
            return okMSG({'data':temp})
        else:
            return failMSG('no such user')

    return failMSG('fail')

def self(request):

    # 检查登录状态
    if 'login_id' not in request.session:
        return failMSG('no login')

    t_uid = request.session['login_id']
    if type(t_uid) != type(1):
        t_uid = int(t_uid)

    # 修改信息
    # 只能用 PUT
    if request.method == 'PUT':

        # 取参数
        try:
            # t_class = request.POST['class']
            t_gender = request.POST['gender']
            t_nickname = request.POST['nickname']
            t_grade = request.POST['grade']
            t_college = request.POST['college']
            t_major = request.POST['major']
            t_studentID = request.POST['studentID']
            t_realname = request.POST['realname']
        except Exception as e:
            return failMSG('parameter error')

        # 数据库操作
        try:
            t_user = User.objects.filter(UserID = t_uid)
        except Exception as e:
            return failMSG('db error')
        else:
            if t_user.count() == 1:
                t_user = t_user[0]
                # t_user.Class = t_class
                t_user.Gender = t_gender
                t_user.Nickname = t_nickname
                t_user.Grade = t_grade
                t_user.College = t_college
                t_user.Major = t_major
                t_user.StudentID = t_studentID
                t_user.RealName = t_realname
                t_user.save()
                return okMSG({'data':temp})
            else:
                return failMSG('no such user')

    # 获取信息
    # 下面只接受 GET
    if request.method != 'GET':
        return failMSG('wrong method')


    # 数据库操作
    try:
        t_user = User.objects.filter(UserID = t_uid)
    except Exception as e:
        return failMSG('db error')
    else:
        if t_user.count() == 1:
            t_user = t_user[0]
            temp = {}
            temp['UserID'] = t_user.UserID
            temp['Email'] = t_user.Email
            # temp['Class'] = t_user.Class
            temp['Gender'] = t_user.Gender
            temp['Nickname'] = t_user.Nickname
            temp['Avatar'] = t_user.Avatar.url
            temp['Description'] = t_user.Description
            temp['Grade'] = t_user.Grade
            temp['College'] = t_user.College
            temp['Major'] = t_user.Major
            temp['StudentID'] = t_user.StudentID
            temp['RealName'] = t_user.RealName
            return okMSG({'data':temp})
        else:
            return failMSG('no such user')

    return failMSG('fail')

def changePassword(request):

    # 要在登录状态下
    if 'login_id' not in request.session:
        return failMSG('no login')
        
    # 仅接受 POST 方法
    if request.method != 'POST':
        return failMSG('wrong method')
        
    # 已经登录, 所以拿取用户信息
    t_uid = request.session['login_id']
    if type(t_uid) != type(1):
        t_uid = int(t_uid)

    # 获取参数
    try:
        old_password = request.PUT['old_password']
        new_password = request.PUT['new_password']
    except Exception as e:
        return failMSG('POST parameter error')
        
    # 数据库操作
    try:
        t_user = User.objects.filter(UserID = t_uid, Password = old_password)
    except Exception as e:
        return failMSG('db error')
    else:
        if t_user.count() <= 0:
            return failMSG('old_password error')
        else:
            t_user = t_user[0]
            t_user.Password = new_password
            t_user.save()
            return okMSG()

    return failMSG('fail')

def uploadAvatar(request):

    # 要在登录状态下
    if 'login_id' not in request.session:
        return failMSG('no login')

    if request.method != 'POST':
        return failMSG('wrong method')

    # 已经登录, 所以拿取用户信息
    t_uid = request.session['login_id']
    if type(t_uid) != type(1):
        t_uid = int(t_uid)

    # test
    # t_username = '123'
    # print(request.FILES)

    # 数据库操作
    try:
        t_user = User.objects.filter(UserID = t_uid)
    except Exception as e:
        return failMSG('db error')
    else:
        if t_user.count() <= 0:
            return failMSG('no such user')
        else:
            t_user = t_user[0]
            t_user.Avatar = request.FILES['file']
            t_user.save()
            return okMSG({'url':t_user.Avatar.url})

    return failMSG('fail')

def searchUser(t_uid):
    
    # 从数据库查找 id = uid 的用户
    # 存在则返回, 否则返回 None
    try:
        t_user = User.objects.filter(UserID = t_uid)
    except Exception as e:
        return None, 'db error'
    else:
        if t_user.count() == 1:
            return t_user[0], None
        return None, 'no such user'