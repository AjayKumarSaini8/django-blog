from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
from django.urls import reverse  # Add this import

User = get_user_model()

class BlogPost(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    
    title = models.CharField(max_length=200)
    content = CKEditor5Field('Content', config_name='extends')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this blog post."""
        return reverse('post_detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            counter = 1
            while BlogPost.objects.filter(slug=self.slug).exclude(id=self.id).exists():
                self.slug = f"{slugify(self.title)}-{counter}"
                counter += 1
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
