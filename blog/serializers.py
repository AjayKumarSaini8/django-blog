from rest_framework import serializers
from .models import BlogPost
from users.serializers import UserSerializer

class BlogPostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at', 'status', 'slug']
        read_only_fields = ['author', 'created_at', 'updated_at', 'slug']
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)