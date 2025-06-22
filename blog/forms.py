from django import forms
from .models import BlogPost
from django_ckeditor_5.widgets import CKEditor5Widget

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
    
    # REMOVE THIS __init__ METHOD COMPLETELY
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Make sure slug field is not required in the form
    #     self.fields['slug'].required = False