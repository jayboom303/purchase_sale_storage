from django.shortcuts import render, redirect
from pss_homepage.models import *

# Create your views here.

#用户登陆
def sign_in_views(request):
    if request.method == 'GET':
        return render(request, 'sign-in.html')
    else:
        account = request.POST.get('account', '')
        upwd = request.POST.get('upwd', '')
        if account=='' or account.isspace():
            message = '提示: 账号不能为空'
            return render(request, 'sign-in.html', locals())
        elif upwd=='' or upwd.isspace():
            message = '提示: 密码不能为空'
            return render(request, 'sign-in.html', locals())

        user = User.objects.filter(account=account, upwd=upwd)
        if user:
            if user[0].is_active == True:
                request.session['id'] = user[0].id
                request.session['account'] = user[0].account
                try:
                    if user[0].role.permission.permission_level == '一级':
                        return redirect('/manager')
                    elif user[0].role.permission.permission_level == '二级':
                        return redirect('')
                    elif user[0].role.permission.permission_level == '三级':
                        return redirect('')
                    else:
                        return redirect('')
                except:
                    return redirect('')
            else:
                message = '提示: 您的账号已暂停服务'
                return render(request, 'sign-in.html', locals())
        else:
            message = '提示: 账号或密码错误,请重试'
            return render(request, 'sign-in.html', locals())
		
#用户退出
def sign_out_views(request):
    del request.session['id']
    del request.session['account']
    return redirect('/sign-in')