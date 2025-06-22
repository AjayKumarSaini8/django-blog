from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from blog.views import (
    BlogPostListView, 
    BlogPostDetailView, 
    BlogPostCreateView, 
    BlogPostUpdateView, 
    BlogPostDeleteView
)
from django.contrib.auth.views import LoginView
from users.views import UserRegistrationView
from django.contrib.auth.decorators import login_required
from blog.views import custom_upload 
from utils.file_upload import CustomFileUploadView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', BlogPostListView.as_view(), name='home'),
    path('posts/new/', BlogPostCreateView.as_view(), name='post_create'),  # Moved up
    path('posts/<slug:slug>/', BlogPostDetailView.as_view(), name='post_detail'),
    path('posts/<slug:slug>/edit/', BlogPostUpdateView.as_view(), name='post_edit'),
    path('posts/<slug:slug>/delete/', BlogPostDeleteView.as_view(), name='post_delete'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    # Keep only one login path (choose either):
    path('login/', auth_views.LoginView.as_view(
        template_name='users/login.html',
        redirect_authenticated_user=True,
        next_page='home'
    ), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('api/auth/', include('users.urls')),
    path('api/blog/', include('blog.urls')),
    path('accounts/profile/', login_required(TemplateView.as_view(
        template_name='users/profile.html'
    )), name='profile'),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
     path('ckeditor5/upload/', custom_upload, name='ck_editor_5_upload_file'),
      # Add CKEditor 5 URL pattern
    path('ckeditor5/upload/', CustomFileUploadView.as_view(), name='ck_editor_5_upload_file'),
]

# Add media URL for development
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)