from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from django.urls import reverse
from django.db.models import Q

from .models import *

def UTIL_ARequests(selected_items, option):
    try:
        if selected_items:
            if option == '1':
                for i in selected_items:
                    Articles.objects.filter(Q(id=i) & Q(status=False)).update(status=True)
            elif option == '2':
                for i in selected_items:
                    Articles.objects.filter(Q(id=i) & Q(status=False)).delete()
    except ValueError:
        pass

class UTIL_DetailMixin:
    model = None
    template = None
    form = None

    def get(self, request, slug):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        f = self.form()
        return render(request, self.template, context={'article': obj, 'form' : f})

    def post(self, request, slug):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        f = self.form(request.POST)
        if f.is_valid():
            new_obj = f.save(commit=False)
            new_obj.author = request.user
            new_obj.post = obj
            new_obj.save()
            return redirect(reverse('articles_detail', kwargs={'slug' : slug}))
        return render(request, self.template, {'form' : f, 'article' : obj})    

class UTIL_CreateMixin:
    model = None
    template = None

    def get(self, request):
        form = self.model()
        return render(request, self.template, context={'form': form})

    def post(self, request):
        bound_form = self.model(request.POST)

        if bound_form.is_valid():
            var = bound_form.save(commit=False)
            var.author = request.user
            var.save()
            return redirect(var)
        return render(request, self.template, context={'form': bound_form})

class UTIL_UpdateMixin:
    model = None
    model_form = None
    template = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(instance=obj)
        key = 'u' + self.model.__name__.lower()
        return render(request, self.template, context={'form':bound_form, key:obj}) 

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(request.POST, instance=obj)

        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        key = 'u' + self.model.__name__.lower()
        return render(request, self.template, context={'form':bound_form, key:obj}) 

class UTIL_DeleteMixin:
    model = None
    template = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        key = 'd' + self.model.__name__.lower()
        return render(request, self.template, context={key:obj}) 

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        obj.delete()

        return redirect(reverse('Homepage'))