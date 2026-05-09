from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    author_display = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author_display', 'is_anonymous', 'content', 'like_count', 'is_liked', 'created_at']
        read_only_fields = ['id', 'like_count', 'created_at']

    def get_author_display(self, obj):
        if obj.is_anonymous:
            return '匿名用户'
        return obj.author.nickname

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
