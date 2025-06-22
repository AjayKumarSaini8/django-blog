from django.db import migrations
from django.utils.text import slugify

def generate_slugs(apps, schema_editor):
    BlogPost = apps.get_model('blog', 'BlogPost')
    for post in BlogPost.objects.filter(slug=''):
        post.slug = orig = slugify(post.title)
        counter = 1
        while BlogPost.objects.filter(slug=post.slug).exclude(id=post.id).exists():
            post.slug = f'{orig}-{counter}'
            counter += 1
        post.save()

class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0002_alter_blogpost_slug'),  # This should point to your previous blog migration
    ]

    operations = [
        migrations.RunPython(generate_slugs),
    ]