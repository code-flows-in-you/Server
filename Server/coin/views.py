# Create your views here.
import json
from .models import UserCoin, CoinFlow
from account.views import okMSG, failMSG, searchUser
from account.models import User
import time

def self(request):

    # 检查登录状态
    if 'login_id' not in request.session:
        return failMSG('no login')

    t_uid = int(request.session['login_id'])

    # GET 方法
    # 获取coin数量
    if request.method == 'GET':
        try:
            t_user = User.objects.filter(UserID = t_uid)
        except Exception as e:
            return failMSG('db error')
        else:
            if t_user.count() == 1:
                t_user = t_user[0]
                t_coins = t_user.coins.all()[0].Coin
                return okMSG({'coin':t_coins})
            else:
                return failMSG('no such user')

    # POST 方法
    # 充值100闲钱
    if request.method == 'POST':
        try:
            t_user = User.objects.filter(UserID = t_uid)
        except Exception as e:
            return failMSG('db error')
        else:
            if t_user.count() == 1:
                t_coin = t_user[0].coins.all()[0]
                t_coin.Coin = t_coin.Coin + 100
                t_coin.save()
                # flow
                t_flow = CoinFlow.objects.create(
                    Uid = t_user[0],
                    Title = '充值',
                    Type = 'Recharge',
                    TimeStamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    Flow = 100
                )
                return okMSG({'coin':t_coin.Coin})
            else:
                return failMSG('no such user')

    # DELETE 方法
    # 弄丢50闲钱
    if request.method == 'DELETE':
        try:
            t_user = User.objects.filter(UserID = t_uid)
        except Exception as e:
            return failMSG('db error')
        else:
            if t_user.count() == 1:
                t_coin = t_user[0].coins.all()[0]
                if t_coin.Coin >= 50:
                    t_coin.Coin = t_coin.Coin - 50
                    t_coin.save()
                    # flow
                    t_flow = CoinFlow.objects.create(
                        Uid = t_user[0],
                        Title = '丢失',
                        Type = 'lose',
                        TimeStamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                        Flow = -50
                    )
                    return okMSG({'coin':t_coin.Coin})
                return failMSG('not enough coin')
            else:
                return failMSG('no such user')

    return failMSG('method error')

def transaction(request, t_uid):

    # 检查登录状态
    if 'login_id' not in request.session:
        return failMSG('no login')

    # 检查方法
    if request.method != 'POST':
        return failMSG('method error')

    self_uid = request.session['login_id']

    try:
        rdata = json.loads(request.body)
    except Exception as e:
        return failMSG('get json data error')

    try:
        tra_coins = rdata['coin']
    except Exception as e:
        return failMSG('parameter error')
    
    try:
        t_user = User.objects.filter(UserID = self_uid)
        o_user = User.objects.filter(UserID = t_uid)
    except Exception as e:
        return failMSG('db error')
    else:
        if t_user.count() == 1 and o_user.count() == 1:
            t_coin = t_user[0].coins.all()[0]
            if t_coin.Coin > tra_coins:
                o_coin = o_user[0].coins.all()[0]
                t_coin.Coin = t_coin.Coin - tra_coins
                o_coin.Coin = o_coin.Coin + tra_coins
                t_coin.save()
                o_coin.save()
                # flow
                t_flow = CoinFlow.objects.create(
                    Uid = t_user[0],
                    Title = '交易',
                    Type = 'transaction',
                    TimeStamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    Flow = -tra_coins
                )
                # flow
                t_flow = CoinFlow.objects.create(
                    Uid = o_user[0],
                    Title = '交易',
                    Type = 'transaction',
                    TimeStamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    Flow = tra_coins
                )
                return okMSG({'coin':t_coin.Coin})
            else:
                return failMSG('not enough coin')
        else:
            return failMSG('error when search user')

    return failMSG('fail')

def payCoin(t_user, t_coin):

    # 如果 t_user 是 uid
    # 则先获取相应的 model
    if type(t_user) == type(1):
        t_user, err = searchUser(t_user)
        if err:
            return err

    # 获取 coin model
    # 进行支付
    try:
        t_user = t_user.coins.all()[0]
    except Exception as e:
        return 'ForeignKey error'
    
    if t_user.Coin >= t_coin:
        t_user.Coin = t_user.Coin - t_coin 
        t_user.save()
        return None 

    return 'not enough coin'

# 检查是否有足够的闲钱
def checkDeposit(t_user, t_coin):

    # 如果 t_user 是 uid
    # 则先获取相应的 model
    if type(t_user) == type(1):
        t_user, err = searchUser(t_user)
        if err:
            return err

    try:
        t_user = t_user.coins.all()[0]
    except Exception as e:
        return 'ForeignKey error'
    
    if t_user.Coin >= t_coin:
        return None 

    return 'not enough coin'

def flow(request):
    # 检查登录状态
    if 'login_id' not in request.session:
        return failMSG('no login')

    # 检查方法
    if request.method != 'GET':
        return failMSG('method error')

    t_uid = request.session['login_id']

    t_user, err = searchUser(t_uid)
    if err:
        return failMSG(err)

    try:
        t_flow = t_user.cf.all()
    except Exception as e:
        print(e)
        return failMSG('db error when get flow')
    else:
        response = {}
        response['flows'] = []

        try:
            for t_f in t_flow:
                temp = {}
                temp['title'] = t_f.Title
                temp['type'] = t_f.Type
                temp['flow'] = t_f.Flow
                temp['timestamp'] = t_f.TimeStamp
                response['flows'].append(temp)
        except Exception as e:
            print(e)
            return failMSG('create flow fail')
        else:
            return okMSG(response)

    return failMSG('fail')
