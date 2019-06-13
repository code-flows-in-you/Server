from account.views import *
import json
from .models import Problem, Answer, Best
from assignment.models import Assignment
from assignment.views import getAsg
from coin.views import checkDeposit
import logging

def publish(request):
    # 检查登录状态
    if 'login_id' not in request.session:
        return failMSG('no login')

    # 检查 method
    if request.method != 'POST':
        return failMSG('wrong method')

    # 从 session 获取 uid
    t_uid = request.session['login_id']

    try:
        rdata = json.loads(request.body)
    except Exception as e:
        return failMSG('get json data error')

    # 从 body 获取参数
    try:
        t_title = rdata['title']
        t_description = rdata['description']
        t_type = 'qa'
        t_creator = t_uid
        t_coin = rdata['coin']
        t_createTime = rdata['createTime']
        t_startTime = rdata['startTime']
        t_endTime = rdata['endTime']
        t_detail = rdata['detail']
    except Exception as e:
        return failMSG('parameter error')

    # 检查用户和闲钱
    t_creator, err = searchUser(t_creator)
    if err:
        return failMSG(err)
    err = checkDeposit(t_creator, t_coin)
    if err:
        return failMSG(err)

    # 创建 assignment
    try:
        t_asg = Assignment.objects.create(
            Title = t_title,
            Description = t_description,
            Type = t_type,
            Creator = t_creator,
            Coins = t_coin,
            CreateTime = t_createTime,
            StartTime = t_startTime,
            EndTime = t_endTime
        )
    except Exception as e:
        return failMSG('create asg fail')

    # 创建 Problem
    try:
        t_pro = Problem.objects.create(
            Aid = t_asg,
            Detail = t_detail
        )
    except Exception as e:
        return failMSG('create problem fail')

    return okMSG({'aid':t_asg.Aid})

def controller(request, t_aid):
    
    # GET 方法, 不用登录
    # 获取懂了么
    if request.method == 'GET':
        response, err = getQAResponse(t_aid)
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

    # delete 方法, 删除懂了么
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

    # POST 方法, 提交懂了么回答
    if request.method == 'POST':

        try:
            rdata = json.loads(request.body)
        except Exception as e:
            return failMSG('get json data error')

        try:
            t_pid = rdata['pid']
            t_value = rdata['answer']
            t_timestamp = rdata['timestamp']
        except Exception as e:
            return failMSG('body parameter error')

        # 取 user asg pro 的 model
        t_user, err = searchUser(t_uid)
        if err:
            return failMSG(err)
        t_asg, err = getAsg(t_aid)
        if err:
            return failMSG(err)
        t_pro, err = getPro(t_pid)
        if err:
            return failMSG(err)

        # 创建 answer
        try:
            t_ans = Answer.objects.create(
                Aid = t_asg,
                Pid = t_pro,
                Uid = t_user,
                Value = t_value,
                TimeStamp = t_timestamp
            )
        except Exception as e:
            print(e)
            return failMSG('create qanswer error')

        return okMSG()

    return failMSG('wrong method')

def answerHelper(request, t_aid, t_qaid):
    # 检查登录状态
    if 'login_id' not in request.session:
        return failMSG('no login')

    # 从 session 获取 uid
    t_uid = request.session['login_id']
    if type(t_uid) != type(1):
        t_uid = int(t_uid)

    # PUT 方法, 采纳回答
    if request.method == 'PUT':
        # 拿到 assignment
        t_asg, err = getAsg(t_aid)
        if err:
            return failMSG(err)

        # 检查 creator
        if t_asg.Creator.UserID != t_uid:
            return failMSG('not creator')

        # 获取 qanswer
        t_ans, err = getAnswer(t_qaid)
        if err:
            return failMSG(err)

        # 检查重复, 一个 asg 只能有一个 best
        if t_asg.qab.count() > 0:
            return failMSG('already have a best answer')

        # 创建 best
        try:
            t_best = Best.objects.create(
                Aid = t_ans.Aid,
                Pid = t_ans.Pid,
                Uid = t_ans.Uid,
                Value = t_ans.Value,
                TimeStamp = t_ans.TimeStamp
            )
        except Exception as e:
            return failMSG('create best fail')

        # best user 获得 coin 奖励
        try:
            t_c = t_ans.Uid.coins.all()[0]
            t_c.Coin += t_ans.Aid.Coins
            t_c.save()
        except Exception as e:
            return failMSG('only give coin fail')
        
        
        return okMSG()

    # delete 方法, 删除懂了么回答
    if request.method == 'DELETE':

        # 获取 qanswer
        t_ans, err = getAnswer(t_qaid)
        if err:
            return failMSG(err)

        # 检查是否是本人回答的
        if t_ans.Uid.UserID != t_uid:
            return failMSG('not your answer')

        # 删除
        t_ans.delete()

        return okMSG()

    return failMSG('wrong method')

def getPro(t_pid):
    # 检查类型
    if type(t_pid) != type(0):
        return None, 'not integer'

    try:
        t_pro = Problem.objects.filter(Pid = t_pid)
    except Exception as e:
        return None, 'db error when get pro'
    else:
        if t_pro.count() == 1:
            return t_pro[0], None
        else:
            return None, 'no such pro'

    return None, 'fail'

def getAnswer(t_qaid):
    # 检查类型
    if type(t_qaid) != type(0):
        return None, 'not integer'

    try:
        t_ans = Answer.objects.filter(QAid = t_qaid)
    except Exception as e:
        return None, 'db error when get qans'
    else:
        if t_ans.count() == 1:
            return t_ans[0], None
        else:
            return None, 'no such qans'

    return None, 'fail'

def getQAResponse(t_aid):
    response = {}
    t_asg, err = getAsg(t_aid)
    if err:
        return None, err

    try:
        t_best = t_asg.qab.all()
        t_answers = t_asg.qas.all()
        t_problem = t_asg.pro.all()[0]
    except Exception as e:
        return None, 'get answers or best fail'

    try:
        response['title'] = t_asg.Title
        response['description'] = t_asg.Description
        response['type'] = t_asg.Type
        response['aid'] = t_asg.Aid
        response['creator'] = t_asg.Creator.Nickname
        response['coin'] = t_asg.Coins
        response['createTime'] = t_asg.CreateTime
        response['startTime'] = t_asg.StartTime
        response['endTime'] = t_asg.EndTime
        response['pid'] = t_problem.Pid
        response['detail'] = t_problem.Detail
        response['best'] = {}
        response['answers'] = []
    except Exception as e:
        return None, 'create dict fail'
    
    try:
        for qas in t_answers:
            temp = {}
            temp['qaid'] = qas.QAid
            temp['aid'] = qas.Aid.Aid
            temp['pid'] = qas.Pid.Pid
            temp['user'] = '%d@%s' % (qas.Uid.UserID, qas.Uid.Nickname)
            temp['timestamp'] = qas.TimeStamp
            temp['answer'] = qas.Value
            response['answers'].append(temp)

        if t_best.count() > 0:
            t_best = t_best[0]
            temp = {}
            temp['aid'] = t_best.Aid.Aid
            temp['pid'] = t_best.Pid.Pid
            temp['user'] = '%d@%s' % (t_best.Uid.UserID, t_best.Uid.Nickname)
            temp['timestamp'] = t_best.TimeStamp
            temp['answer'] = t_best.Value
            response['best'] = temp

    except Exception as e:
        logging.error(e)
        return None, 'get qa fail'

    return response, None