from django.urls import path
from .views import *

urlpatterns = [
    path('', Articles_list.as_view(), name='Homepage'),
    path('article/requests/', Article_requests.as_view(), name="article_requests_url"),
    path('article/create/', ArticleCreate.as_view(), name='article_create_url'),
    path('article/<str:slug>/', ArticleDetail.as_view(), name='articles_detail'),
    path('article/<str:slug>/edit/', ArticleEdit.as_view(), name='article_edit_url'),
    path('article/<str:slug>/delete/', ArticleDelete.as_view(), name='article_delete_url'), 
    path('tag/create/', TagCreate.as_view(), name='tag_create_url'),
    path('tag/<str:slug>/edit/', TagEdit.as_view(), name='tag_edit_url'),
    path('tag/<str:slug>/delete/', TagDelete.as_view(), name='tag_delete_url')
]