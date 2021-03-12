from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name = "login"),
    path('register/', views.register, name = "register"),
    path('logout/', views.logout_user, name="logout"),
    path('profile/update/', views.profile_update, name="profile_update"),
    path('profile/<user>/', views.profile_detail, name="profile_detail"),
    path('admin/articles/', views.admin_articles, name="admin_articles"),
    path('admin/users/', views.admin_users, name="admin_users"),
    path('admin/servers/', views.admin_servers, name="admin_servers"),
]