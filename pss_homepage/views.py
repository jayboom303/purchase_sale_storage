from django.shortcuts import render, redirect
from tools.common import my_login_required

# Create your views here.

# 首页
@my_login_required
def no_permission_views(request,user):

    if user:
        if user.is_active == True:
            request.session['id'] = user.id
            request.session['account'] = user.account
            try:
                if user.role.permission.permission_level == '一级':
                    return redirect('/manager')
                elif user.role.permission.permission_level == '二级':
                    return redirect('')
                elif user.role.permission.permission_level == '三级':
                    return redirect('')
                else:
                    return render(request, 'no-permission.html', locals())
            except:
                return render(request, 'no-permission.html', locals())
        else:
            return redirect('/sign-in')
    else:
        return redirect('/sign-in')

@my_login_required
def upcoming_views(request,user):
      
    return render(request,'upcoming.html',locals())
