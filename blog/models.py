from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.

class Tag(models.Model):
    name = models.CharField('Тег', max_length=256, blank=True, null=True)
    description = models.TextField('Описание', null=True, blank=True)
    url = models.SlugField(max_length=256, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

class Category(models.Model):
    name = models.CharField('Наименование', max_length=256, blank=True, null=True)
    description = models.TextField('Описание', null=True, blank=True)
    url = models.SlugField(max_length=256, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Article(models.Model):
    tags = models.ManyToManyField(Tag, null=True, blank=True, verbose_name='Теги')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Категория', related_name='category_articles')
    headline = models.CharField("Заголовок", max_length=800, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    text = RichTextField('Содержимое статьи', null=True, blank=True)
    views = models.PositiveBigIntegerField('Просмотры', null=True, blank=True, default=0)
    picture = models.ImageField('Заставка', upload_to='articles/', null=True, blank=True)
    url = models.SlugField(max_length=800, unique=True)

    def __str__(self):
        return self.headline

    def get_comments(self):
        return self.article_comments.filter(parent__isnull=True)

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ['-date']


class Comment(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', blank=True, null=True, related_name='user_comments')
    parent = models.ForeignKey('self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True, related_name='self_comments')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Статья', related_name='article_comments')
    text = models.TextField('Сообщение')
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.customer.username + " - " + self.text

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


class Mailing(models.Model):
    email = models.EmailField('Адрес электронной почты', max_length=400, blank=True, null=True)

    def __str__(self):
        return str(self.email)
