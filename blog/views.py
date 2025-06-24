from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from .models import BlogPost
from rest_framework import generics, permissions
from .serializers import BlogPostSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Q  # Added Q import
from django.views.generic import CreateView
from .forms import BlogPostForm

# blog/views.py (add this at the bottom)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.utils.text import slugify

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Like, Comment
from .forms import CommentForm

@csrf_exempt
@login_required
def custom_upload(request):
    # Add file type validation
    allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
    
    # Add file size limit (5MB)
    max_size = 5 * 1024 * 1024  # 5MB
    
    # Get the uploaded file
    uploaded_file = request.FILES.get('upload')
    
    # Perform validations
    if uploaded_file:
        # Check file type
        if uploaded_file.content_type not in allowed_types:
            return JsonResponse({
                'error': {
                    'message': 'Invalid file type. Only images are allowed.'
                }
            }, status=400)
        
        # Check file size
        if uploaded_file.size > max_size:
            return JsonResponse({
                'error': {
                    'message': f'File too large. Max size is {max_size//1024//1024}MB.'
                }
            }, status=400)
    
    # Call the original upload handler
    return image_upload(request)

@login_required
@require_POST
def like_post(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'like_count': post.like_count,
            'is_liked': created
        })
    return redirect('post_detail', slug=slug)

from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

@login_required
@require_POST
def add_comment(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    form = CommentForm(request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
    
    return redirect('post_detail', slug=slug)

# Class-based view alternative (optional)
class CustomUploadView(View):
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def post(self, request):
        return image_upload(request)

# Frontend Views
class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = BlogPost.objects.filter(status='published')
        if self.request.user.is_authenticated:
            user_posts = BlogPost.objects.filter(author=self.request.user)
            queryset = queryset | user_posts

        # Add search functionality
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(content__icontains=search_query)
            )

        return queryset.distinct().order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context

class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_authenticated:
            return queryset.filter(status='published')
        return queryset.filter(
            Q(status='published') | 
            Q(author=self.request.user)
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['user_has_liked'] = self.object.user_has_liked(self.request.user)
        return context

class BlogPostCreateView(LoginRequiredMixin, CreateView):
    form_class = BlogPostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        # Generate slug from title
        if not form.instance.slug:
            base_slug = slugify(form.instance.title)
            form.instance.slug = base_slug
            counter = 1
            # Ensure slug is unique
            while BlogPost.objects.filter(slug=form.instance.slug).exists():
                form.instance.slug = f"{base_slug}-{counter}"
                counter += 1
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('home')

class BlogPostUpdateView(LoginRequiredMixin, UpdateView):
    model = BlogPost 
    form_class = BlogPostForm  # Use form_class instead of fields
    template_name = 'blog/post_form.html'
    context_object_name = 'form'
    slug_field = 'slug'
    
    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)
    
    def get_success_url(self):
        return reverse('post_detail', kwargs={'slug': self.object.slug})

class BlogPostDeleteView(LoginRequiredMixin, DeleteView):
    model = BlogPost
    template_name = 'blog/post_confirm_delete.html'
    slug_field = 'slug'
    success_url = reverse_lazy('home')
    
    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)

# API Views
class BlogPostListAPIView(generics.ListCreateAPIView):
    queryset = BlogPost.objects.filter(status='published')
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            user_posts = BlogPost.objects.filter(author=self.request.user)
            queryset = queryset | user_posts
        return queryset.distinct().order_by('-created_at')

class BlogPostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_object(self):
        obj = get_object_or_404(BlogPost, slug=self.kwargs['slug'])
        if obj.status != 'published' and obj.author != self.request.user:
            self.permission_denied(self.request)
        return obj