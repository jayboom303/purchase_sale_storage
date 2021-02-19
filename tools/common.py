from pss_homepage.models import User
from django.shortcuts import redirect

def my_login_required(func):
    '''自定义 登录验证 装饰器'''
    def check_login_status(request):
        '''检查登录状态'''
        if 'id' in request.session and 'account' in request.session:
            id = request.session['id']
            account = request.session['account']
            user = User.objects.filter(id=id, account=account)[0]
            if user:
                if user.is_active == True:
					# 当前有用户登录，正常跳转
                    return func(request,user)
                else:
                    return redirect('/sign-in')
            else:
                return redirect('/sign-in')

        else:
            # 当前没有用户登录，跳转到登录页面
            return redirect('/sign-in')
            # return HttpResponseRedirect('/sign_in')
            
    return check_login_status

