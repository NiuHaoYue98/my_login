from django.shortcuts import render,render_to_response
from django import forms
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from login.models import User

# Create your views here.
class UserForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=100)
    password = forms.CharField(label='密码', widget=forms.PasswordInput())

def regist(req):
    if req.method == 'POST':
        # 如果有Post提交的动作，就酱Post中的数据值赋给uf，共该函数使用
        uf = UserForm(req.POST)
        if uf.is_valid():
            # 获取表单数据
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            # 添加到数据库
            registAdd = User.obkects.get_or_create(username=username, password=password)

            if registAdd == False:
                return render_to_response('share.html',{'registAdd':registAdd,'username':'username'})
            else:
                return render_to_response('share.html',{'registAdd':registAdd})
    else:
            uf = UserForm()
    return render_to_response('regist.html',{'uf':uf},context_instance=RequestContext(req))

def login(req):
    if req.method == 'POST':
        uf = UserForm(req.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            # 对比提交的数据与数据库中的数据
            user = User.objects.fliter(username__exact = username, password__exact = password)
             if user:
                 #比较成功，跳转到index页面
                 # 这里和网页中的代码示例不一样
                return render_to_response(req,'index.html')
                # 对比成功后将username写入浏览器cookie，失效时间为3600
                response.set_cookie('username',username,3600)
             else:
                 # 这里也和网页中的范例写得不一样，是和mooc的一样
                 return render_to_response(req,'login.html')
    else:
        uf = UserForm()
    return render_to_response('login')

def index(req):
    username = req.COOKIES.get('username','')
    return render_to_response('index/html',{'username':username})

def logout(req):
    response = HttpResponse('logout!!!')
    #清除cookie里保存的username
    response.delete_cookie('username')
    return response

def share(req):
    if req.method == 'POST':
        uf = UserForm(req.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']

            return render_to_response('share.html',{'username':username})
    else:
        uf = UserForm()
    return render_to_response('share.html',{'uf':uf})