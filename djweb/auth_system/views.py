from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import logout, authenticate
from django.contrib.auth import login as auth_login
from .forms import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.http import HttpResponse
from .models import *
from articles.models import Comments, Articles
from servers.models import Servers
from django.db.models import Q
from django.contrib.auth.models import User

def admin_articles(request):
    articles = Articles.objects.all()
    return render(request, 'auth_system/admin_articles.html', {'articles' : articles})

def admin_users(request):
    users = User.objects.all()
    return render(request, 'auth_system/admin_users.html', {'users' : users})

def admin_servers(request):
    servers = Servers.objects.all()
    return render(request, 'auth_system/admin_servers.html', {'servers' : servers})

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=user, password=password)
            auth_login(request, user)
            return redirect(reverse('Homepage'))
    else:
        form = RegisterForm()

    return render(request = request,
                        template_name = "auth_system/register.html",
                        context={"form":form})

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            us = authenticate(request, username=username, password=password)
            if us is not None:
                if us.is_active:
                    auth_login(request, us)
                    return redirect(reverse('Homepage'))
                else:
                    return HttpResponse("You're account is disabled.")
            else:
                return render(request = request,
                        template_name = "auth_system/login.html",
                        context={"form":form, 'error': '0'})
    else:
        form = LoginForm()

    return render(request = request,
                        template_name = "auth_system/login.html",
                        context={"form":form})

@login_required
def logout_user(request):
    logout(request)
    return render(request = request,
                        template_name = "auth_system/logout.html")

def profile_detail(request, user):
    ui = get_object_or_404(User, username__iexact=user)
    group_queries = ui.groups.all()
    group = None

    comms = Comments.objects.filter(author=ui).order_by('date_pub')
    latest_comments = comms.reverse()[:5]

    posts = Articles.objects.filter(author=ui).order_by('date_pub')
    latest_posts = posts.reverse()[:5]

    for i in group_queries:
        group = i

    context = {
        'ui' : ui, 
        'latest_comments' : latest_comments, 
        'latest_posts' : latest_posts,
        'group' : group,
    }
    
    return render(request, 'auth_system/profile_detail.html', context)

@login_required
def profile_update(request):
    obj  = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            
            x = form.cleaned_data.get('x')
            y = form.cleaned_data.get('y')
            width = form.cleaned_data.get('width')
            height = form.cleaned_data.get('height')
            if width or height:
                resizing(obj.img, x, y, width, height)

            return render(request, 'auth_system/profile_detail.html', {'ui' : request.user, 'success' : True})
    else:
        form = ProfileUpdateForm(instance=obj)

    return render(request, 'auth_system/profile_update.html', {'form' : form})