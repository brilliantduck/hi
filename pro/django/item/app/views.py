import hashlib
import os
import string
import random
import math

import requests
from django.shortcuts import render
from django.urls import reverse
from .models import User
from .forms import LoginForm, SignupForm
from django.http import HttpResponseRedirect, HttpResponse, StreamingHttpResponse
from datetime import timedelta
from django.utils import timezone
from .models import User, File
from django.shortcuts import get_list_or_404, get_object_or_404
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO


def signup(request):
    """
    注册页面
    """
    error_msg = ''
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if User.objects.filter(username=username):
                error_msg = 'user %s exists' % username
                return render(request, 'app/signup.html',
                              context={'error_msg':error_msg})
            else:
                User.objects.create(username = username, password=password)
                login_url = reverse('app:login')
                return HttpResponseRedirect(redirect_to=login_url)
    else:
        form = SignupForm()
    context = {'form':form, 'error_msg':error_msg,
            'title':'Sign up', 'submit_value': 'Sign up'}
    return render(request, 'app/signup.html', context=context)


def gen_sid(text):
    """
    生成session的sha1码
    """
    return hashlib.sha1(text.encode()).hexdigest()


def login(request):
    """
    登录窗口，判断用户是否存在
    """
    if request.method == 'POST':
        #  import pdb
        #  pdb.set_trace()
        form = LoginForm(request.POST)
        if form.is_valid():
            #检测验证码
            posted_captcha = form.cleaned_data['captcha']
            saved_captcha = request.session.get('captcha')
            if saved_captcha is None:
                return HttpRseponse('验证码错误')
            #对比验证码
            if posted_captcha.lower() == saved_captcha:
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                if User.objects.filter(username=username, password=password):
                    #登录成功之后，设置session
                    delta = timedelta(days=1)
                    exprie_time = timezone.now() + delta
                    session_data = exprie_time.strftime('%s')
                    session_id = gen_sid('%s:%s' % (username, session_data))
                    request.session[session_id] = session_data
                    index_url = reverse('app:index')
                    response = HttpResponseRedirect(redirect_to=index_url)
                    response.set_cookie('sid', session_id,
                                        int(delta.total_seconds()))
                    response.set_cookie('name', username)
                    return response
            else:
                form.add_error('captcha','验证码不匹配')
    else:
        form = LoginForm()
    context = {'form': form,'title': 'login', 'submit_value':'Login'}
    return render(request, "app/login.html", context=context)


def make_image(char):
    '''
    验证码的基本设置信息
    '''
    im_size = (70, 40)
    font_size = 28
    bg = (0, 0, 0)
    offset = (1, 1)
    im = Image.new('RGB', size=im_size, color=bg)
    font = ImageFont.truetype('app/ubuntu.ttf', font_size)
    draw = ImageDraw.ImageDraw(im)
    draw.text(offset, char, fill='yellow', font=font)
    im = im.transform(im_size, Image.AFFINE, (1, -0.3, 0, -0.1, 1, 0), Image.BILINEAR)
    return im

def captcha(request):
    '''
    渲染验证码页面
    '''
    text = gentext(4)
    request.session['captcha'] = text.lower()#把验证码内容,加到session中用于判断
    im = make_image(text)
    imgout = BytesIO()
    im.save(imgout, format='png')
    img_bytes = imgout.getvalue()
    return HttpResponse(img_bytes, content_type='image/png')


def gentext(n):
    '''
    随机生成4个字母
    '''
    chars = string.ascii_letters
    return ''.join([random.choice(chars) for i in range(n)])

def is_login(request):
    '''
    判断是否够登录
    '''
    sid = request.COOKIES.get('sid', None)
    if sid is None:
        return False
    try:
        expire_second = int(request.session[sid])
    except KeyError:
        return False
    #查看session过期时间是否已经过了
    current_second = int(timezone.now().strftime('%s'))
    if expire_second < current_second:
        return False
    return True

def page(request, page):
    """
    分页
    """
    files = File.objects.all().order_by('filename')
    name = request.COOKIES.get('name', None)
    pages = math.ceil(len(files) / 5)
    if int(page) < 1 or int(page) > pages:
        context = {'error_msg':'找不到页面'}
        return render(request, 'app/page.html', context)
    else:
        fis_page = True
        las_page = True
        if int(page) == 1:
            fis_page = False
        if int(page) == pages:
            las_page = False
        context = {'data':files[(int(page)-1)*5:(int(page)*5)],
                   'tiele':'page','name':name, 'upper':int(page)-1,
                   'lower':int(page)+1, 'fis_page':fis_page,'las_page':las_page}
        return render(request, 'app/page.html', context=context)

        #  if len(files) >= 5:
            #  if (len(files) % 5) == 0:
                #  z_page = len(files) // 5
            #  else:
                #  z_page = (len(files) // 5) + 1
            #  if 1 <= int(page) <= z_page:
                #  context = {'data':files[(int(page)-1)*5:(int(page)*5)],
                           #  'tiele':'page','name':name}
                #  return render(request, 'app/page.html', context=context)
            #  else:
                #  context = {'error_msg':'找不到页面'}
                #  return render(request, 'app/page.html', context=context)
        #  else:
            #  context = {'data':files[:], 'title':'page', 'name':name}
            #  return render(request, 'app/page.html', context=context)

def index(request):
    """
    检测用户是否已经登录
    """
    login_is = is_login(request)
    if login_is:
        name = request.COOKIES.get('name', None)
        files = get_list_or_404(File)
        context={'data':files[0:5],'title':'index','login_is':login_is,
                 'name':name}
        return render(request,'app/index.html',context=context)
    else:
        files = get_list_or_404(File)
        return render(request, 'app/index.html',
                context={'data':files, 'login_is':login_is})

def detail(request, pk):
    """
    上传文件详情
    """
    login_is = is_login(request)
    if login_is:
        name = request.COOKIES.get('name', None)
        file = get_object_or_404(File, pk=pk)
        context = {'data':file,'title':'detail','name':name,'login_is':login_is}
        return render(request, 'app/detail.html',context=context)
    else:
        file = get_object_or_404(File, pk=pk)
        context={'data':file,'title':'detail'}
        return render(request, 'app/detail.html', context=context)

def logout(request):
    '''
    推出登录，删除session, 也可以把cookie也删除
    '''
    sid = request.COOKIES.get('sid', None)
    if sid is not None:
        del request.session[sid]
    return HttpResponseRedirect(redirect_to=reverse('app:index'))

def file_md5(path):
    """
    生成md5码
    """
    m = hashlib.md5()
    text = open(path, 'rb').read()
    m.update(text)
    return m.hexdigest()

def upload(request):
    """
    文件上传
    :param request:
    :return:
    """
    login_is = is_login(request)
    if login_is:
        if request.method == 'POST':
            myFile = request.FILES.get("myfile", None)
            if myFile is None:
                return render(request, 'app/index.html',
                              context={'erorr':'文件不存在'})

            """
            /tmp/files/  设置文件上传的路径 wind的系统估计和linux不一样，具体设
            置
            """
            files = open(os.path.join("/tmp/files/", myFile.name), 'wb+')
            for chunk in myFile.chunks(chunk_size=1024):
                files.write(chunk)
            files.close()

            filepath = "/tmp/files/%s" % myFile.name
            is_status = os.path.getsize(filepath)
            if is_status == myFile.size:
                status = 1
            else:
                status = 0
            md5 = file_md5(filepath)
            username=User.objects.get(username=request.COOKIES.get('name'))
            File.objects.create(filename=myFile.name, owner=username,
                                size=myFile.size, status=status, path=filepath,
                                md5=md5)
            #file_status = '上传完成'
            return HttpResponseRedirect(redirect_to=reverse('app:index'))
    else:
        return HttpResponseRedirect(redirect_to=reverse('app:login'))

def download(request, pk):
    login_is = is_login(request)
    if login_is:
        file = get_object_or_404(File, pk=pk)
        filepath = file.path
        filename = file.filename
        new_file = open(filepath, 'rb')

        #  def file_download(filepath, chunk_size=1024):
            #  with open(filepath, 'rb') as f:
                #  while True:
                    #  c = f.read(chunk_size)
                    #  if c:
                        #  yield c
                    #  else:
        #                  break
        #  new_file_name = filename
        response = StreamingHttpResponse(new_file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(filename)
        return response
    else:
        return HttpResponseRedirect(redirect_to=reverse('app:login'))

