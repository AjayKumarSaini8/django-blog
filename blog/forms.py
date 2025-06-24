from django import forms
from .models import BlogPost
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your comment here...'
            })
        }

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'status']  # Only these fields are included
        widgets = {
            'content': CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"},
                config_name="extends"
            )
        }
