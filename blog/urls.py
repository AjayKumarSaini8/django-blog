from django.urls import path
from .views import BlogPostListView, BlogPostDetailView
from .views import like_post, add_comment

urlpatterns = [
    path('posts/', BlogPostListView.as_view(), name='post-list'),
    path('posts/<slug:slug>/', BlogPostDetailView.as_view(), name='post-detail'),
    path('', BlogPostListView.as_view(), name='home'),
     path('posts/<slug:slug>/like/', like_post, name='like_post'),
    path('posts/<slug:slug>/comment/', add_comment, name='add_comment'),
]