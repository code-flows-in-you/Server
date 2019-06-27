from account.views import okMSG, failMSG, searchUser
from .models import Assignment
from questionnaire.models import Answer, Options, Questions

def getRecent(request):
    # 检查 method
    if request.method != 'GET':
        return failMSG('wrong method')

    response, err = getAllAsgResponse()
    if err:
        return failMSG(err)

    return okMSG(response)


def getRecentByPages(request, t_pages):
    # 检查 method
    if request.method != 'GET':
        return failMSG('wrong method')

    response, err = getAsgResponse((t_pages-1)*20, 20)
    if err:
        return failMSG(err)

    return okMSG(response)

def getAllAsgResponse():
    response = {}
    response['assignments'] = []
    # 数据库操作
    try:
        t_asg = Assignment.objects.all().order_by('-CreateTime')
    except Exception as e:
        return None, 'db error when get rec asg'
    else:
        for asg in t_asg:
            temp = {}
            temp['title'] = asg.Title
            temp['description'] = asg.Description
            temp['type'] = asg.Type
            temp['aid'] = asg.Aid
            temp['creator'] = asg.Creator.Nickname
            temp['coin'] = asg.Coins
            temp['createTime'] = asg.CreateTime
            temp['startTime'] = asg.StartTime
            temp['endTime'] = asg.EndTime
            temp['answerCount'] = 0
            temp['bestCount'] = 0
            temp['unit'] = 0
            temp['copy'] = 0
            if asg.Type == 'qa':
                temp['answerCount'] = asg.qas.all().count()
                temp['bestCount'] = asg.qab.all().count()
            else:
                temp['unit'] = asg.qnncoin.all()[0].Coin
                temp['copy'] = asg.qnncoin.all()[0].Copy
            response['assignments'].append(temp)
        response['asgCount'] = Assignment.objects.all().count()
        return response, None

    return None, 'fail'

def getAsgResponse(start, count):
    # 简单检查
    if start < 0 or count <= 0:
        return None, 'parameter error'

    response = {}
    response['assignments'] = []
    # 数据库操作
    try:
        # t_asg = Assignment.objects.all().reverse()[start:start+count]
        # t_asg = Assignment.objects.all()[start:start+count]
        t_asg = Assignment.objects.all().order_by('-CreateTime')[start:start+count]
    except Exception as e:
        return None, 'db error when get rec asg'
    else:
        for asg in t_asg:
            temp = {}
            temp['title'] = asg.Title
            temp['description'] = asg.Description
            temp['type'] = asg.Type
            temp['aid'] = asg.Aid
            temp['creator'] = asg.Creator.Nickname
            temp['coin'] = asg.Coins
            temp['createTime'] = asg.CreateTime
            temp['startTime'] = asg.StartTime
            temp['endTime'] = asg.EndTime
            temp['answerCount'] = 0
            temp['bestCount'] = 0
            temp['unit'] = 0
            temp['copy'] = 0
            if asg.Type == 'qa':
                temp['answerCount'] = asg.qas.all().count()
                temp['bestCount'] = asg.qab.all().count()
            else:
                temp['unit'] = asg.qnncoin.all()[0].Coin
                temp['copy'] = asg.qnncoin.all()[0].Copy
            response['assignments'].append(temp)
        response['asgCount'] = Assignment.objects.all().count()
        return response, None

    return None, 'fail'

def deleteAsgByAid(t_asg):

    # 如果 t_asg 是 aid
    # 则先获取相应的 model
    if type(t_asg) == type(1):
        try:
            t_asg = Assignment.objects.filter(Aid = t_asg)
        except Exception as e:
            return 'asg db error'

        if t_asg.count() == 1:
            t_asg = t_asg[0]
        else:
            return 'no such Assignment'

    try:
        t_asg.delete()
    except Exception as e:
        return 'delete error'

    return None

 
def getAsg(t_aid):
    # 检查类型
    if type(t_aid) != type(0):
        return None, 'not integer'

    try:
        t_asg = Assignment.objects.filter(Aid = t_aid)
    except Exception as e:
        return None, 'db error when get asg'
    else:
        if t_asg.count() == 1:
            return t_asg[0], None
        else:
            return None, 'no such asg'

    return None, 'fail'

def getAsgResponseByClass(start, count, t_type = 'questionnaire'):
    # 简单检查
    if start < 0 or count <= 0:
        return None, 'parameter error'

    if t_type != 'questionnaire' and t_type != 'qa':
        return None, 'type error'

    response = {}
    response['assignments'] = []
    # 数据库操作
    try:
        t_asg = Assignment.objects.filter(Type = t_type).order_by('-CreateTime')[start:start+count]
    except Exception as e:
        return None, 'db error when get rec asg'
    else:
        for asg in t_asg:
            temp = {}
            temp['title'] = asg.Title
            temp['description'] = asg.Description
            temp['type'] = asg.Type
            temp['aid'] = asg.Aid
            temp['creator'] = asg.Creator.Nickname
            temp['coin'] = asg.Coins
            temp['createTime'] = asg.CreateTime
            temp['startTime'] = asg.StartTime
            temp['endTime'] = asg.EndTime
            temp['answerCount'] = 0
            temp['bestCount'] = 0
            temp['unit'] = 0
            temp['copy'] = 0
            if asg.Type == 'qa':
                temp['answerCount'] = asg.qas.all().count()
                temp['bestCount'] = asg.qab.all().count()
            else:
                temp['unit'] = asg.qnncoin.all()[0].Coin
                temp['copy'] = asg.qnncoin.all()[0].Copy
            response['assignments'].append(temp)
        response['asgCount'] = Assignment.objects.filter(Type = t_type).count()
        return response, None

    return None, 'fail'

def getAllAsgResponseByClass(t_type = 'questionnaire'):

    if t_type != 'questionnaire' and t_type != 'qa':
        return None, 'type error'

    response = {}
    response['assignments'] = []
    # 数据库操作
    try:
        t_asg = Assignment.objects.filter(Type = t_type).order_by('-CreateTime')
    except Exception as e:
        return None, 'db error when get rec asg'
    else:
        for asg in t_asg:
            temp = {}
            temp['title'] = asg.Title
            temp['description'] = asg.Description
            temp['type'] = asg.Type
            temp['aid'] = asg.Aid
            temp['creator'] = asg.Creator.Nickname
            temp['coin'] = asg.Coins
            temp['createTime'] = asg.CreateTime
            temp['startTime'] = asg.StartTime
            temp['endTime'] = asg.EndTime
            temp['answerCount'] = 0
            temp['bestCount'] = 0
            temp['unit'] = 0
            temp['copy'] = 0
            if asg.Type == 'qa':
                temp['answerCount'] = asg.qas.all().count()
                temp['bestCount'] = asg.qab.all().count()
            else:
                temp['unit'] = asg.qnncoin.all()[0].Coin
                temp['copy'] = asg.qnncoin.all()[0].Copy
            response['assignments'].append(temp)
        response['asgCount'] = Assignment.objects.filter(Type = t_type).count()
        return response, None

    return None, 'fail'

def getRecentByClass(request, t_class):
    # 检查 method
    if request.method != 'GET':
        return failMSG('wrong method')

    response, err = getAllAsgResponseByClass(t_class)
    if err:
        return failMSG(err)

    return okMSG(response)

def getRecentByClassAndPages(request, t_class, t_pages):
    # 检查 method
    if request.method != 'GET':
        return failMSG('wrong method')

    response, err = getAsgResponseByClass((t_pages-1)*20, 20, t_class)
    if err:
        return failMSG(err)

    return okMSG(response)

def getMyAsg(request, t_class):
    # 检查 method
    if request.method != 'GET':
        return failMSG('wrong method')

    # 检查登录状态
    if 'login_id' not in request.session:
        return failMSG('no login')

    # 从 session 获取 uid
    t_uid = int(request.session['login_id'])

    # 检查 get 参数
    if t_class != 'all' and t_class != 'questionnaire' and t_class != 'qa' and t_class != 'answer':
        return failMSG('parameter error')

    if t_class == 'all':
        response = {}
        response['assignments'] = []
        t_user, err = searchUser(t_uid)
        if err:
            return failMSG(err)

        # 数据库操作
        try:
            t_asg = t_user.asg.all().order_by('-CreateTime')
        except Exception as e:
            return failMSG('db error when get my asg')
        else:
            for asg in t_asg:
                temp = {}
                temp['title'] = asg.Title
                temp['description'] = asg.Description
                temp['type'] = asg.Type
                temp['aid'] = asg.Aid
                temp['creator'] = asg.Creator.Nickname
                temp['coin'] = asg.Coins
                temp['createTime'] = asg.CreateTime
                temp['startTime'] = asg.StartTime
                temp['endTime'] = asg.EndTime
                temp['answerCount'] = 0
                temp['bestCount'] = 0
                temp['unit'] = 0
                temp['copy'] = 0
                if asg.Type == 'qa':
                    temp['answerCount'] = asg.qas.all().count()
                    temp['bestCount'] = asg.qab.all().count()
                else:
                    temp['unit'] = asg.qnncoin.all()[0].Coin
                    temp['copy'] = asg.qnncoin.all()[0].Copy
                response['assignments'].append(temp)
            response['asgCount'] = t_asg.count()
            return okMSG(response)
        return failMSG('fail')

    if t_class == 'questionnaire' or t_class == 'qa':
        response = {}
        response['assignments'] = []
        t_user, err = searchUser(t_uid)
        if err:
            return failMSG(err)

        # 数据库操作
        try:
            t_asg = t_user.asg.filter(Type = t_class).order_by('-CreateTime')
        except Exception as e:
            return failMSG('db error when get my asg')
        else:
            for asg in t_asg:
                temp = {}
                temp['title'] = asg.Title
                temp['description'] = asg.Description
                temp['type'] = asg.Type
                temp['aid'] = asg.Aid
                temp['creator'] = asg.Creator.Nickname
                temp['coin'] = asg.Coins
                temp['createTime'] = asg.CreateTime
                temp['startTime'] = asg.StartTime
                temp['endTime'] = asg.EndTime
                temp['answerCount'] = 0
                temp['bestCount'] = 0
                temp['unit'] = 0
                temp['copy'] = 0
                if asg.Type == 'qa':
                    temp['answerCount'] = asg.qas.all().count()
                    temp['bestCount'] = asg.qab.all().count()
                else:
                    temp['unit'] = asg.qnncoin.all()[0].Coin
                    temp['copy'] = asg.qnncoin.all()[0].Copy
                response['assignments'].append(temp)
            response['asgCount'] = t_asg.count()
            return okMSG(response)
        return failMSG('fail')

    if t_class == 'answer':
        response = {}
        response['assignments'] = []
        t_user, err = searchUser(t_uid)
        if err:
            return failMSG(err)

        t_ans = t_user.qas.all()

        try:
            t_asg = set()

            for x in t_ans:
                t_asg.add(x.Aid)
            
            for asg in t_asg:
                temp = {}
                temp['title'] = asg.Title
                temp['description'] = asg.Description
                temp['type'] = asg.Type
                temp['aid'] = asg.Aid
                temp['creator'] = asg.Creator.Nickname
                temp['coin'] = asg.Coins
                temp['createTime'] = asg.CreateTime
                temp['startTime'] = asg.StartTime
                temp['endTime'] = asg.EndTime
                temp['answerCount'] = 0
                temp['bestCount'] = 0
                temp['unit'] = 0
                temp['copy'] = 0
                if asg.Type == 'qa':
                    temp['answerCount'] = asg.qas.all().count()
                    temp['bestCount'] = asg.qab.all().count()
                else:
                    temp['unit'] = asg.qnncoin.all()[0].Coin
                    temp['copy'] = asg.qnncoin.all()[0].Copy
                response['assignments'].append(temp)
            # response['asgCount'] = t_asg.count()
            return okMSG(response)
        except Exception as e:
            print(e)
            return failMSG('my answer fail')

    return failMSG('fail')