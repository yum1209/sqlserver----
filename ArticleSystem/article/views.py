
# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Article, Comment, LikeRecord
from django.http import JsonResponse


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
    return redirect('')


@login_required
def article_list(request):
    query = request.GET.get('q', '')
    if query:
        articles = Article.objects.filter(title__icontains=query)
        if not articles:
            return render(request, 'article/article_list.html', {'articles': articles, 'no_results': True})
    else:
        articles = Article.objects.all()
    return render(request, 'article/article_list.html', {'articles': articles, 'no_results': False})

@login_required
def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    comments = article.comments.all()
    # print(comments) 
    if request.method == 'POST':
        comment_content = request.POST.get('content', '')
        if comment_content:
            Comment.objects.create(article=article, author=request.user, content=comment_content)
            return redirect('article_detail', article_id=article_id)
    return render(request, 'article/article_detail.html', {'article': article, 'comments': comments})

@login_required
def submit_article(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if not title or not content:
            messages.error(request, "标题和内容不能为空！")
        else:
            Article.objects.create(title=title, content=content, author=request.user)
            messages.success(request, "文章提交成功！")
            return redirect('article_list')
    return render(request, 'article/submit_article.html')

@login_required
def manage_article_list(request):
    # 查询当前用户的文章
    user_articles = Article.objects.filter(author=request.user)
    return render(request, 'article/manage_article_list.html', {'articles': user_articles})


@login_required
def edit_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)

    # 确保只有文章作者可以编辑
    if article.author != request.user:
        messages.error(request, "你没有权限修改此文章！")
        return redirect('edit_article_list')

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if not title or not content:
            messages.error(request, "标题和内容不能为空！")
        else:
            article.title = title
            article.content = content
            article.save()
            messages.success(request, "文章修改成功！")
            return redirect('article_detail', article_id=article_id)

    return render(request, 'article/edit_article.html', {'article': article})

def delete_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    article.delete()
    return redirect('article_list')  # Adjust this to redirect to the appropriate page

@login_required
def like_comment(request, article_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user not in comment.likes.all():
        comment.likes.add(request.user)
    else:
        comment.likes.remove(request.user)
    return redirect('article_detail', article_id=article_id)