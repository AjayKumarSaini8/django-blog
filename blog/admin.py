from django.contrib import admin
from .models import BlogPost
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

class BlogPostAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].widget = CKEditor5Widget(
            attrs={"class": "django_ckeditor_5"}, config_name="extends"
        )
    
    class Meta:
        model = BlogPost
        fields = '__all__'

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostAdminForm
    list_display = ('title', 'author', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'author')
    search_fields = ('title', 'content', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)
    
    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        obj.save()