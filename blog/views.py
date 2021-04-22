from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.contrib import messages
from blog.forms import addCommentForm
from blog.models import *


class ArticlesHomeView(ListView):
    template_name = 'blog/main.html'
    model = Article

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        context['popular_articles'] = self.get_queryset().order_by('-views')
        return context


class ArticleDetailView(DetailView):
    model = Article
    slug_field = 'url'
    template_name = 'blog/blog-single.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        context['popular_articles'] = Article.objects.all().order_by('-views')
        return context

    def post(self, request, *args, **kwargs):
        form = addCommentForm(request.POST)
        if form.is_valid():
            form_save = form.save(commit=False)
            form_save.customer = request.user
            form_save.article = self.get_object()
            if request.POST.get("parent", None):
                form_save.parent_id = int(request.POST.get('parent'))
            form_save.save()
            return redirect(f'/article/detail/{self.get_object().url}/#comments')
        else:
            messages.add_message(self.request, messages.INFO, 'Заполните поля.')
            return redirect(f'/article/detail/{self.get_object().url}/#formReview')


class CategoryArcticlesView(ListView):
    template_name = 'blog/category.html'
    model = Article

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        context['popular_articles'] = self.get_queryset().order_by('-views')
        context['category'] = Category.objects.get(url=self.kwargs['name'])
        context['object_list'] = self.get_queryset().filter(category=Category.objects.get(url=self.kwargs['name']))
        return context






