from django.urls import path
from . import views

urlpatterns = [
    path('', views.ArticlesHomeView.as_view(), name='home'),
    path('article/detail/<slug:slug>/', views.ArticleDetailView.as_view(), name='detail-article'),
    # path('article/add/comment/', views.AddCommentView.as_view(), name='add-comment'),
]