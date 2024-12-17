
# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Article, Comment



# home page
def home_view(request):
    # 如果用户已登录，显示主页
    if request.user.is_authenticated:
        return render(request, 'home.html', {'user': request.user})
    
    if request.method == 'POST':
        if 'login' in request.POST:  # 处理登录表单
            username = request.POST.get('login_username')
            password = request.POST.get('login_password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # 登录成功
            else:
                messages.error(request, "登录失败：用户名或密码错误")
        
        elif 'register' in request.POST:  # 处理注册表单
            username = request.POST.get('register_username')
            password1 = request.POST.get('register_password1')
            password2 = request.POST.get('register_password2')
            
            # 验证注册表单数据
            if not username or not password1:
                messages.error(request, "注册失败：用户名和密码不能为空")
            elif password1 != password2:
                messages.error(request, "注册失败：两次密码不一致")
            elif User.objects.filter(username=username).exists():
                messages.error(request, "注册失败：用户名已存在")
            else:
                # 创建新用户
                User.objects.create_user(username=username, password=password1)
                messages.success(request, "注册成功，请登录！")
                return redirect('home')  # 注册成功后刷新页面

    # 如果未登录，渲染登录/注册页面
    return render(request, 'home.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

# 主页，需登录访问
# @login_required
def home(request):
    return render(request, 'home.html', {'user': request.user})

# @login_required
def article_list(request):
    articles = Article.objects.all()
    return render(request, 'article/article_list.html', {'articles': articles})

# @login_required
def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    comments = article.comments.all()
    if request.method == 'POST':
        comment_content = request.POST.get('content', '')
        if comment_content:
            Comment.objects.create(article=article, author=request.user, content=comment_content)
            return redirect('article_detail', article_id=article_id)
    return render(request, 'article/article_detail.html', {'article': article, 'comments': comments})

# @login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user not in comment.likes.all():
        comment.likes.add(request.user)
    return redirect('article_detail', article_id=comment.article.id)