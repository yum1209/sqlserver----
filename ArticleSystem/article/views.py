from django.shortcuts import render
# from .vue_components import MyVueComponent

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Comment
from django.contrib.auth.decorators import login_required

# @login_required
def article_list(request):
    articles = Article.objects.all()
    return render(request, 'article/article_list.html', {'articles': articles})

@login_required
def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    comments = article.comments.all()
    if request.method == 'POST':
        comment_content = request.POST.get('content', '')
        if comment_content:
            Comment.objects.create(article=article, author=request.user, content=comment_content)
            return redirect('article_detail', article_id=article_id)
    return render(request, 'article/article_detail.html', {'article': article, 'comments': comments})

@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user not in comment.likes.all():
        comment.likes.add(request.user)
    return redirect('article_detail', article_id=comment.article.id)