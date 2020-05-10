# -*-coding:utf-8 -*-
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .fetchdata import *
from .makerandstr import *
from .sms import SendSms
from random import randint
import time

def index(request):
    try:
        stockcode = request.GET['stockcode']
    except:
        stockcode = 'sh'
    uid = request.session.get('uid', None)
    return render(request, 'ui/index.html', {**get_stock(stockcode), **get_rf_list(), **get_user_photo(uid) })

def login(request):
    if request.session.get('is_login', None):
        return redirect('/')
    if request.method == "POST":
        if request.POST.get('submitType', None) == "getCode":
            pnum = request.POST.get('pnum', None)
            if not pnum:
                return render(request, 'ui/login.html', {'message':'请输入手机号！'})
            u = UserInfo.objects.get_or_create(phone=pnum)[0]
            if float(u.verifydeadline) < time.time():
                vcode = str(randint(100000,999999))
                u.verifycode = vcode
                u.verifydeadline = str(int(time.time()) + 120)
                u.save()
                SendSms(pnum, vcode)
            else:
                return render(request, 'ui/login.html', {'message':'验证码以发送！'})
        elif request.POST.get('submitType', None) == "messLogin":
            pnum = request.POST.get('pnum', None)
            vcode = request.POST.get('code', None)
            if not pnum or not vcode:
                return render(request, 'ui/login.html', {'message':'请输入手机号及验证码！'})
            try:
                u = UserInfo.objects.get(phone=pnum)
            except:
                return render(request, 'ui/login.html', {'message':'用户不存在！'})
            if float(u.verifydeadline) > time.time() and vcode == u.verifycode:
                if u.name == None:
                    u.name = "用户" + make_rand_str(8)
                if u.passwd == None:
                    u.passwd = make_rand_str(10)
                u.save()
                request.session['is_login'] = True
                request.session['uid'] = u.id
                return redirect('/')
            else:
                return render(request, 'ui/login.html', {'message':'验证码错误！'})
        elif request.POST.get('submitType', None) == "passLogin":
            uname = request.POST.get('uname', None)
            passwd = request.POST.get('pass', None)
            if not uname or not passwd:
                return render(request, 'ui/login.html', {'message':'请输入手机号/邮箱及密码！'})
            try:
                if '@' in uname:
                    u = UserInfo.objects.get(email=uname)
                else:
                    u = UserInfo.objects.get(phone=uname)
            except:
                return render(request, 'ui/login.html', {'message':'用户不存在！'})
            if passwd == u.passwd:
                request.session['is_login'] = True
                request.session['uid'] = u.id
                return redirect('/')
            else:
                return render(request, 'ui/login.html', {'message':'手机号/邮箱或密码错误！'})
            
    return render(request, 'ui/login.html')

def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/')
    request.session.flush()
    return redirect('/')

def pick(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    try:
        uid = request.session.get('uid', None)
        selfstocks = UserInfo.objects.get(id=uid).selfstocks.split(';')
    except:
        request.session.flush()
        return redirect('/login/')
    if request.method == "POST":
        if request.POST.get('submitType',None) == "removeStock":
            scode = request.POST.get('scode',None)
            if scode in selfstocks:
                selfstocks.remove(scode)
            u = UserInfo.objects.get(id = uid)
            u.selfstocks = ";".join(selfstocks)
            u.save()
        elif request.POST.get('submitType',None) == "addStock":
            scode = request.POST.get('scode',None)
            try:
                StockBasic.objects.get(code = scode)
            except:
                return render(request, 'ui/pick.html', {**get_stocks(selfstocks), **get_user_photo(uid), **{'message':'您的输入有误！'} })
            if scode not in selfstocks:
                selfstocks.append(scode)
            u = UserInfo.objects.get(id = uid)
            u.selfstocks = ";".join(selfstocks)
            u.save()
            
    return render(request, 'ui/pick.html', {**get_stocks(selfstocks), **get_user_photo(uid) })

def pick_inner(request):
    try:
        stockcode = request.GET['stockcode']
    except:
        stockcode = None
    if stockcode:
        return render(request, 'ui/pick-stock.html', {**get_stock(stockcode) })
    else:
        return render(request, 'ui/pick-news.html', {**get_news() })
        
def hold(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    try:
        stockcode = request.GET['stockcode']
    except:
        stockcode = '000001'
    uid = request.session.get('uid', None)
    if request.method == "POST":
        if request.POST.get('submitType',None) == "bStock":
            scode = request.POST.get('scode', None)
            sname = request.POST.get('sname', None)
            sprice = request.POST.get('sprice', None)
            svol = request.POST.get('svol', None)
            
            record = Records.objects.create(code = scode, name = sname, bprice = sprice, bvolume = svol)
            u = UserInfo.objects.get(id = uid)
            u.selfrecords = str(record.id) if u.selfrecords == None else u.selfrecords + ";" + str(record.id)
            u.save()
            
            return render(request, 'ui/hold.html', {**get_stock_quote(scode), **get_records(uid), **get_user_photo(uid) })
            
        elif request.POST.get('submitType',None) == "aStock":
            rid = request.POST.get('rid', None)
            ap = request.POST.get('aprice', None)
            scode = request.POST.get('scode', None)
            try:
                record = Records.objects.get(id = rid)
                record.issold = True
                record.aprice = ap
                record.save()
            except:
                pass
            return render(request, 'ui/hold.html', {**get_stock_quote(scode), **get_records(uid), **get_user_photo(uid) })
    return render(request, 'ui/hold.html', {**get_stock_quote(stockcode), **get_records(uid), **get_user_photo(uid) })
    
def predict(request):
    #if not request.session.get('is_login', None):
    #    return redirect('/login/')
    try:
        stockcode = request.GET['stockcode']
    except:
        stockcode = 'sh'
    uid = request.session.get('uid', None)
    return render(request, 'ui/predict.html', {**get_stock(stockcode), **get_user_photo(uid) })
    
def profile(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    try:
        uid = request.session.get('uid', None)
        if not uid:
            request.session.flush()
            return redirect('/login/')
    except:
        request.session.flush()
        return redirect('/login/')
    if request.method == "POST":
        uname = request.POST.get('uname', None)
        uemail = request.POST.get('uemail', None)
        upass = request.POST.get('upass', None)
        uarea = request.POST.get('uarea', None)
        u = UserInfo.objects.get(id = uid)
        u.name = uname if uname else u.name
        u.email = uemail if uemail else u.email
        u.passwd = upass if upass else u.passwd
        u.country = uarea if uarea else u.country
        u.save()
                
    return render(request, 'ui/profile.html', {**get_user_profile(uid), **get_user_photo(uid) })
        
def page_not_found(request, excapetion):
    return render(request, 'ui/pages-error-404.html')


