from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import *
from django.contrib.auth.hashers import make_password
from .models import *
import a2s
import socket
import time
from django.http import Http404

def servers_delete(request, id):
    obj = get_object_or_404(Servers, id=id)

    if request.method == 'POST':
        obj.delete()
        return redirect(reverse('servers_list'))
    else:
        return render(request, 'servers/servers_delete.html', {'obj' : obj})

def servers_change(request, id):
    obj = get_object_or_404(Servers, id=id)

    if request.method == 'POST':
        form = ServersAddForm(request.POST, instance=obj)
        if form.is_valid():
            obj = form.save()
            return redirect(reverse('servers_list'))
    else:
        form = ServersAddForm(instance=obj)

    return render(request, 'servers/servers_change.html', {'form' : form})

def servers_list(request):
    servers = Servers.objects.all()
    k = {}

    for i in servers:
        try:
            k[i.id] = a2s.info((i.ip, i.port))

        except socket.gaierror:
            k[i.id] = False
            continue

        except socket.timeout:
            k[i.id] = False
            continue

    return render(request, 'servers/servers_list.html', {'servers' : k})

def servers_add(request):
    if request.method == 'POST':
        form = ServersAddForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.password = make_password(form.cleaned_data.get('password'), None, 'md5')
            obj.save()

            return redirect(reverse('servers_list'))
    else:
        form = ServersAddForm()

    return render(request, 'servers/servers_add.html', {'form': form})

def servers_detail(request, id):
    obj = get_object_or_404(Servers, id=id)

    try:
        s = a2s.info((obj.ip, obj.port))
        p = a2s.players((obj.ip, obj.port))

        for i in p:
            i.duration = time.strftime("%H:%M:%S", time.gmtime(i.duration))

    except socket.gaierror:
        raise Http404
        
    except socket.timeout:
        raise Http404
    
    return render(request, 'servers/servers_detail.html', {'addr': f'{obj.ip}:{obj.port}', 'players' : p, 'server' : s})
