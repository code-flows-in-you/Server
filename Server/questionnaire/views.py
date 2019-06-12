# Create your views here.

from account.views import okMSG, failMSG, searchUser
from coin.views import checkDeposit
from .models import *
from assignment.models import Assignment
from assignment.views import *
import json

def publish(request):
    # 检查登录状态
    if 'login_id' not in request.session:
        return failMSG('no login')

    # 检查 method
    if request.method != 'POST':
        return failMSG('wrong method')

    # 从 session 获取 uid
    t_uid = int(request.session['login_id'])

    try:
        rdata = json.loads(request.body)
    except Exception as e:
        return failMSG('get json data error')

    # 从 body 获取参数
    try:
        t_title = rdata['title']
        t_description = rdata['description']
        t_type = 'questionnaire'
        t_creator = t_uid
        # 单份问卷的闲钱奖励
        t_coin = int(rdata['coin'])
        # 问卷份数
        t_copy = int(rdata['copy'])
        t_createTime = rdata['createTime']
        t_startTime = rdata['startTime']
        t_endTime = rdata['endTime']
        t_questions = rdata['questions']
        t_options = rdata['options']
    except Exception as e:
        return failMSG('parameter error')

    # 检查用户和闲钱
    t_creator, err = searchUser(t_creator)
    if err:
        return failMSG(err)
    err = checkDeposit(t_creator, t_coin*t_copy)
    if err:
        return failMSG(err)

    # 创建 assignment
    try:
        t_asg = Assignment.objects.create(
            Title = t_title,
            Description = t_description,
            Type = t_type,
            Creator = t_creator,
            Coins = t_coin * t_copy,
            CreateTime = t_createTime,
            StartTime = t_startTime,
            EndTime = t_endTime
        )
    except Exception as e:
        return failMSG('create asg fail')

    # 创建qnn coin
    try:
        t_qc = QnnCoin.objects.create(
            Aid = t_asg,
            Coin = t_coin,
            Copy = t_copy
        )
    except Exception as e:
        return failMSG('create qc fail')

    # 准备创建 question 和 option
    # q_length 有多少个 question
    # has_option 检查每个 question 是否有 option
    # opt_index 下一个创建的 option 序号
    q_length = len(t_questions)
    has_option = False 
    opt_index = 0
    for index in range(q_length):
        # 创建 question
        try:
            temp = t_questions[index]
            t_que = Questions.objects.create(
                Aid = t_asg,
                Title = temp['title'],
                Type = temp['type']
            )
        except Exception as e:
            return failMSG('create question fail')

        # 创建 option
        temp = options[opt_index]
        while temp['questionIndex'] == index:
            has_option = True 
            try:
                t_opt = Options.objects.create(
                    Qid = t_que,
                    Aid = t_asg,
                    Value = temp['value']
                )
            except Exception as e:
                return failMSG('create option fail')
            opt_index += 1

        # 检查是否每个 question 都有 option
        if has_option == False:
            err = deleteAsgByAid(t_asg)
            if err:
                return failMSG('some questions miss option and ' + err)
            return failMSG('some questions miss option')

        has_option = False

    return okMSG({'aid':t_asg.Aid})

def controller(request, t_aid):

    # GET 方法, 不用登录
    # 获取问卷
    if request.method == 'GET':
        response, err = getQuestionnaireResponse(t_aid)
        if err:
            return failMSG(err)

        return okMSG(response)

    # 检查登录状态
    if 'login_id' not in request.session:
        return failMSG('no login')

    # 从 session 获取 uid
    t_uid = request.session['login_id']
    if type(t_uid) != type(1):
        t_uid = int(t_uid)

    # delete 方法, 删除问卷
    if request.method == 'DELETE':
        # 拿到 model
        t_asg, err = getAsg(t_aid)
        if err:
            return failMSG(err)

        # 检查 creator
        if t_asg.Creator.UserID == t_uid:
            t_asg.delete()
            return okMSG()
        else:
            return failMSG('not creator')

    # POST 方法, 提交问卷答案
    if request.method == 'POST':

        try:
            rdata = json.loads(request.body)
        except Exception as e:
            return failMSG('get json data error')

        try:
            t_answers = rdata['answers']
        except Exception as e:
            return failMSG('body parameter error')

        # 检查是否已经回答
        err = alreadyAnswer(t_uid, t_aid)
        if err:
            return failMSG(err)

        # 取 user asg 的 model
        t_user, err = searchUser(t_uid)
        if err:
            return failMSG(err)
        t_asg, err = getAsg(t_aid)
        if err:
            return failMSG(err)

        # 创建 answer
        for ans in t_answers:
            print(ans)
            print(ans['qid'])
            t_que, err = getQuestion(ans['qid'])
            if err:
                delAns(t_uid, t_aid)
                return failMSG(err)
            t_opt, err = getOption(ans['oid'])
            if err:
                delAns(t_uid, t_aid)
                return failMSG(err)

            try:
                t_ans = Answer.objects.create(
                    Oid = t_opt,
                    Qid = t_que,
                    Aid = t_asg,
                    Uid = t_user,
                    Value = ans['value'],
                    TimeStamp = ans['timestamp']
                )
            except Exception as e:
                delAns(t_uid, t_aid)
                return failMSG('db error when create answer')

        # 获得1闲钱报酬
        try:
            t_c = t_user.coins.all()[0]
            t_one = t_asg.qnncoin.all()[0]
            t_c.Coin += t_one.Coin
            t_asg.Coins -= t_one.Coin
            t_c.save()
            t_asg.save()
        except Exception as e:
            return failMSG('only get coin fail')

        return okMSG()

    return failMSG('wrong method')

def getAnswerByAid(request, t_aid):
    # 检查登录状态
    if 'login_id' not in request.session:
        return failMSG('no login')

    # 从 session 获取 uid
    t_uid = request.session['login_id']
    if type(t_uid) != type(1):
        t_uid = int(t_uid)

    t_asg, err = getAsg(t_aid)
    if err:
        return failMSG(err)

    # 检查 creator
    # 只有 creator 可以查看统计答案
    if t_asg.Creator.UserID != t_uid:
        return failMSG('not creator')

    # 获取问卷信息
    response, err = getQuestionnaireResponse(t_aid)
    if err:
        return failMSG(err)

    # 获取 aid=t_aid 的 options
    try:
        t_options = Options.objects.filter(Aid = t_aid)
    except Exception as e:
        return failMSG('db error when get options')
    else:
        if t_options.count() > 0:
            for os in t_options:
                response[str(os.oid)] = []
                t_answers = os.ans.all() 
                for answer in t_answers:
                    temp = {}
                    temp['user'] = '%d@%s' % (answer.Uid.UserID, answer.Uid.Nickname)
                    temp['value'] = answer.Value
                    temp['timestamp'] = answer.TimeStamp
                    response[str(os.oid)].append(temp)

            return okMSG()
        else:
            return failMSG('no options')

    return failMSG('fail')

# 通过 qid 获取 questions
def getQuestion(t_qid):
    # 检查类型
    if type(t_qid) != type(0):
        return None, 'not integer'

    try:
        t_que = Questions.objects.filter(Aid = t_qid)
    except Exception as e:
        return None, 'db error when get question'
    else:
        if t_que.count() == 1:
            return t_que[0], None
        else:
            return None, 'no such question'

    return None, 'fail'


# 通过 oid 获取 options
def getOption(t_oid):
    # 检查类型
    if type(t_oid) != type(0):
        return None, 'not integer'

    try:
        t_opt = Options.objects.filter(Aid = t_oid)
    except Exception as e:
        return None, 'db error when get question'
    else:
        if t_opt.count() == 1:
            return t_opt[0], None
        else:
            return None, 'no such question'

    return None, 'fail'

def delAns(t_uid, t_aid):
    # 检查类型
    if type(t_uid) != type(0) or type(t_aid) != type(0):
        return 'not integer'

    try:
        t_ans = Answer.objects.filter(Uid__UserID = t_uid, Aid__Aid = t_aid)
    except Exception as e:
        return 'db error when del answers'
    else:
        if t_ans.count() > 0:
            t_ans.delete()
        else:
            return 'no ans to del'

    return None

def alreadyAnswer(t_uid, t_aid):
    # 检查类型
    if type(t_uid) != type(0) or type(t_aid) != type(0):
        return 'not integer'

    try:
        t_ans = Answer.objects.filter(Uid__UserID = t_uid, Aid__Aid = t_aid)
    except Exception as e:
        return 'db error when check answers'
    else:
        if t_ans.count() > 0:
            return 'already answer'

    return None

def getQuestionnaireResponse(t_aid):
    response = {}
    t_asg, err = getAsg(t_aid)
    if err:
        return None, err

    try:
        t_questions = t_asg.qnn.all()
        t_options = t_asg.opt.all()
    except Exception as e:
        return None, 'get question or option fail'

    try:
        response['title'] = t_asg.Title
        response['description'] = t_asg.Description
        response['type'] = t_asg.Type
        response['aid'] = t_asg.Aid
        response['creator'] = t_asg.Creator.Nickname
        response['coin'] = t_asg.Coins
        response['unit'] = t_asg.qnncoin.all()[0].Coin
        response['createTime'] = t_asg.CreateTime
        response['startTime'] = t_asg.StartTime
        response['endTime'] = t_asg.EndTime
        response['questions'] = []
        response['options'] = []
    except Exception as e:
        return None, 'create dict fail'
    
    try:
        for qs in t_questions:
            temp = {}
            temp['qid'] = qs.Qid
            temp['aid'] = qs.Aid.Aid
            temp['title'] = qs.Title
            temp['type'] = qs.Type
            response['questions'].append(temp)

        for os in t_options:
            temp = {}
            temp['oid'] = os.Oid
            temp['qid'] = os.Qid.Qid
            temp['aid'] = os.Aid.Aid
            temp['value'] = os.Value
            response['options'].append(temp)
    except Exception as e:
        print(e)
        return None, 'create qs or os fail'

    

    return response, None