from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import ChatRoom, Message, Report
from .serializers import ChatRoomSerializer, MessageSerializer, ReportSerializer
from matching.models import Match
from users.models import BlackList


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def room_list(request):
    rooms = ChatRoom.objects.filter(
        Q(match__user_a=request.user) | Q(match__user_b=request.user),
        is_active=True,
    ).select_related('match__user_a', 'match__user_b').order_by('-last_message_at')
    serializer = ChatRoomSerializer(rooms, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def room_messages(request, room_id):
    try:
        room = ChatRoom.objects.get(id=room_id)
    except ChatRoom.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.user not in (room.match.user_a, room.match.user_b):
        return Response(status=status.HTTP_403_FORBIDDEN)

    messages = room.messages.order_by('created_at')
    return Response(MessageSerializer(messages, many=True).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_image(request, room_id):
    try:
        room = ChatRoom.objects.get(id=room_id)
    except ChatRoom.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.user not in (room.match.user_a, room.match.user_b):
        return Response(status=status.HTTP_403_FORBIDDEN)

    image = request.FILES.get('image')
    if not image:
        return Response({'detail': '请上传图片'}, status=status.HTTP_400_BAD_REQUEST)

    msg = Message.objects.create(
        chat_room=room,
        sender=request.user,
        msg_type=Message.MsgType.IMAGE,
        content=image.name,
    )
    msg.content = request.build_absolute_uri(f'/media/chat/{image.name}')

    from django.core.files.storage import default_storage
    default_storage.save(f'chat/{image.name}', image)
    msg.save()

    return Response(MessageSerializer(msg).data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def report_user(request):
    serializer = ReportSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({'detail': '举报已提交，我们会尽快处理'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def block_user(request, user_id):
    from users.models import User
    try:
        target = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if target == request.user:
        return Response({'detail': '不能屏蔽自己'}, status=status.HTTP_400_BAD_REQUEST)

    BlackList.objects.get_or_create(blocker=request.user, blocked=target)
    ChatRoom.objects.filter(
        Q(match__user_a=request.user, match__user_b=target) |
        Q(match__user_a=target, match__user_b=request.user)
    ).update(is_active=False)

    return Response({'detail': f'已屏蔽 {target.nickname}'})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def unblock_user(request, user_id):
    BlackList.objects.filter(blocker=request.user, blocked_id=user_id).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

