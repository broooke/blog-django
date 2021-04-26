from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.html import strip_tags
from django.views.generic import TemplateView, ListView, DetailView, CreateView, FormView
from django.contrib import messages
from django.views.generic.base import View

from blog.forms import addCommentForm
from blog.models import *


class ArticlesHomeView(ListView):
    template_name = 'blog/main.html'
    model = Article
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        context['popular_articles'] = self.get_queryset().order_by('-views')[:5]
        context['latest_articles'] = self.get_queryset().annotate(num_comments=Count('article_comments')).order_by('-num_comments', '-views')[:4]
        context['most_comments'] = self.get_queryset().annotate(num_comments=Count('article_comments')).order_by('-num_comments')[:3]
        context['most_views_comments'] = self.get_queryset().annotate(num_comments=Count('article_comments')).order_by('-num_comments', '-views')[:10]
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
        context['object_list'] = self.get_queryset().filter(category=Category.objects.get(url=self.kwargs['name']))
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        context['popular_articles'] = self.get_queryset().order_by('-views')
        context['category'] = Category.objects.get(url=self.kwargs['name'])
        return context


class ContactView(TemplateView):
    template_name = 'blog/contact.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        context['popular_articles'] = Article.objects.all().order_by('-views')
        return context

    def post(self, request):
        try:
            template = render_to_string('extends/email_dict.html', {
                'name': self.request.POST.get('name'),
                'headline': self.request.POST.get('phone'),
                'email': self.request.POST.get('email'),
                'message': self.request.POST.get('message'),
            })

            text_content = strip_tags(template)

            email = EmailMultiAlternatives(
                self.request.POST.get('phone'),
                text_content,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER]
            )

            email.attach_alternative(template, "text/html")
            email.send()
            messages.add_message(self.request, messages.SUCCESS, 'Сообщение отправлено!')
        except:
            messages.add_message(self.request, messages.ERROR, 'Возникла ошибка, попробуйте позже')

        return redirect('contact')


class ServicesView(TemplateView):
    template_name = 'blog/services.html'