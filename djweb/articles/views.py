from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View

from .models import *
from .utils import *
from .forms import *
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.paginator import Paginator

from django.db.models import Q


class Article_requests(PermissionRequiredMixin, View):

    permission_required = 'articles.can_approve'

    def get(self, request):
        articles = Articles.objects.filter(status=False)
        return render(request, 'articles/articles_requests.html', {'articles': articles})

    def post(self, request, *args, **kwargs):
        selected_items = request.POST.getlist('article_id[]')
        option = request.POST.get('select')
        articles = Articles.objects.filter(status=False)

        UTIL_ARequests(selected_items, option)

        context = {
            'articles' : articles, 
            'selected_items' : selected_items,
            'option' : option,
        }

        return render(request, 'articles/articles_requests.html', context)

class Articles_list(View):
    def get(self, request):
        search_query = request.GET.get('search', '')

        if search_query:
            articles = Articles.objects.filter(Q(title__icontains=search_query)
                                            | Q(body__icontains=search_query)
                                            & Q(status=True))
        else:
            articles = Articles.objects.filter(status=True)

        pending_count = Articles.objects.filter(status=False).count()
        paginator = Paginator(articles, 4)
        page_number = request.GET.get('page', 1)
        page = Paginator.get_page(paginator, page_number)

        context={
            'articles' : page, 
            'pending_count' : pending_count,
        }
        
        return render(request, 'articles/index.html', context)

class ArticleDetail(UTIL_DetailMixin, View):
    model = Articles
    form = CommentsForm
    template = 'articles/article_detail.html'

class TagCreate(LoginRequiredMixin, UTIL_CreateMixin, View):
    model = TagForm
    template = 'articles/tag_create.html'
    raise_exception = True

class ArticleCreate(UTIL_CreateMixin, View):
    model = ArticlesForm
    template = 'articles/articles_create.html'

class TagEdit(LoginRequiredMixin, UTIL_UpdateMixin, View):
    model = Tag
    model_form = TagForm
    template = 'articles/tag_edit.html'
    raise_exception = True

class ArticleEdit(LoginRequiredMixin, UTIL_UpdateMixin, View):
    model = Articles
    model_form = ArticlesForm
    template = 'articles/article_edit.html'
    raise_exception = True

class ArticleDelete(LoginRequiredMixin, UTIL_DeleteMixin, View):
    model = Articles
    template = 'articles/article_delete.html'
    raise_exception = True

class TagDelete(LoginRequiredMixin, UTIL_DeleteMixin, View):
    model = Tag
    template = 'articles/tag_delete.html'
    raise_exception = True
