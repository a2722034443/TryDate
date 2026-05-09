from rest_framework import serializers
from users.serializers import UserProfileSerializer
from .models import Match


class MatchSerializer(serializers.ModelSerializer):
    partner = serializers.SerializerMethodField()
    my_action = serializers.SerializerMethodField()
    is_expired = serializers.SerializerMethodField()

    class Meta:
        model = Match
        fields = [
            'id', 'partner', 'compatibility_score', 'dimension_scores',
            'compatibility_highlights', 'my_action', 'status',
            'week_number', 'matched_at', 'action_deadline', 'is_expired',
        ]

    def get_partner(self, obj):
        request = self.context.get('request')
        user = request.user
        partner = obj.user_b if obj.user_a == user else obj.user_a
        data = UserProfileSerializer(partner, context={'request': request}).data
        if obj.status != Match.MatchStatus.MATCHED:
            data.pop('avatar_url', None)
        return data

    def get_my_action(self, obj):
        user = self.context['request'].user
        return obj.get_action_for(user)

    def get_is_expired(self, obj):
        from django.utils import timezone
        return timezone.now() > obj.action_deadline and obj.status == Match.MatchStatus.PENDING
