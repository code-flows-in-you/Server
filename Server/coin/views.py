# Create your views here.
import json
from .models import UserCoin
from account.views import okMSG, failMSG, searchUser

def self(request):

    # 检查登录状态
    if 'login_id' not in request.session:
        return failMSG('no login')

    t_uid = request.session['login_id']

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

