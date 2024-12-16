from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),
    path('comment/<int:comment_id>/like/', views.like_comment, name='like_comment'),
]