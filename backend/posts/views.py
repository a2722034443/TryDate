from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Post, PostLike
from .serializers import PostSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def post_list(request):
    posts = Post.objects.filter(status=Post.PostStatus.ACTIVE).order_by('-created_at')
    serializer = PostSerializer(posts, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    serializer = PostSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_like(request, post_id):
    try:
        post = Post.objects.get(id=post_id, status=Post.PostStatus.ACTIVE)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    like, created = PostLike.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
        Post.objects.filter(id=post_id).update(like_count=post.likes.count())
        return Response({'liked': False, 'like_count': post.likes.count()})

    Post.objects.filter(id=post_id).update(like_count=post.likes.count())
    return Response({'liked': True, 'like_count': post.likes.count()})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id, author=request.user)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    post.status = Post.PostStatus.DELETED
    post.save(update_fields=['status'])
    return Response(status=status.HTTP_204_NO_CONTENT)

