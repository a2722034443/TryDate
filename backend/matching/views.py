from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Match
from .serializers import MatchSerializer
from .tasks import run_weekly_match, get_week_number


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_match(request):
    week = get_week_number()
    match = Match.objects.filter(
        week_number=week
    ).filter(
        Q(user_a=request.user) | Q(user_b=request.user)
    ).first()

    if not match:
        return Response({'detail': '本周缘分还在路上～', 'matched': False})

    return Response({'matched': True, 'match': MatchSerializer(match, context={'request': request}).data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def respond_match(request, match_id):
    action = request.data.get('action')
    if action not in (Match.Action.LIKED, Match.Action.PASSED):
        return Response({'detail': '无效操作'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        match = Match.objects.get(id=match_id)
    except Match.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.user not in (match.user_a, match.user_b):
        return Response(status=status.HTTP_403_FORBIDDEN)

    if match.status != Match.MatchStatus.PENDING:
        return Response({'detail': '该匹配已结束'}, status=status.HTTP_400_BAD_REQUEST)

    if timezone.now() > match.action_deadline:
        match.status = Match.MatchStatus.MISSED
        match.save(update_fields=['status'])
        return Response({'detail': '确认时间已过期'}, status=status.HTTP_400_BAD_REQUEST)

    if match.get_action_for(request.user) != Match.Action.PENDING:
        return Response({'detail': '已经操作过了'}, status=status.HTTP_400_BAD_REQUEST)

    match.set_action_for(request.user, action)
    return Response(MatchSerializer(match, context={'request': request}).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def match_history(request):
    matches = Match.objects.filter(
        Q(user_a=request.user) | Q(user_b=request.user)
    ).order_by('-matched_at')
    serializer = MatchSerializer(matches, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def trigger_match(request):
    if not request.user.is_staff:
        return Response(status=status.HTTP_403_FORBIDDEN)
    count = run_weekly_match()
    return Response({'detail': f'匹配完成，生成 {count} 对'})
