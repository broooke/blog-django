from django.urls import path
from . import views

urlpatterns = [
    path('', views.ArticlesHomeView.as_view(), name='home'),
    path('article/detail/<slug:slug>/', views.ArticleDetailView.as_view(), name='detail-article'),
    # path('article/add/comment/', views.AddCommentView.as_view(), name='add-comment'),
    path('articles/category/<str:name>/', views.CategoryArcticlesView.as_view(), name='articles-category'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('services/', views.ServicesView.as_view(), name='services'),
]