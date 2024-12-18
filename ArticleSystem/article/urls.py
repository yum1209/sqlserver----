from django.urls import path
from . import views

urlpatterns = [
    # 用户相关
    path('', views.home_view, name='home'),  # 主页，包含登录/注册或欢迎页面
    path('logout/', views.logout_view, name='logout'),  # 退出登录

    # 文章相关
    path('articles/', views.article_list, name='article_list'),  # 文章列表
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),  # 文章详情
    path('article/<int:article_id>/like_comment/<int:comment_id>/', views.like_comment, name='article_comment'), # 文章评论点赞
]