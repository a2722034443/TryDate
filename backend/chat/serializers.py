from rest_framework import serializers
from .models import ChatRoom, Message, Report


class MessageSerializer(serializers.ModelSerializer):
    sender_nickname = serializers.CharField(source='sender.nickname', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender_id', 'sender_nickname', 'msg_type', 'content', 'created_at']
        read_only_fields = ['id', 'sender_id', 'sender_nickname', 'created_at']


class ChatRoomSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    partner = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = ['id', 'partner', 'last_message', 'unread_count', 'last_message_at', 'created_at']

    def get_partner(self, obj):
        from users.serializers import UserProfileSerializer
        user = self.context['request'].user
        partner = obj.get_other_user(user)
        return UserProfileSerializer(partner, context=self.context).data

    def get_last_message(self, obj):
        msg = obj.messages.order_by('-created_at').first()
        if msg:
            return MessageSerializer(msg).data
        return None

    def get_unread_count(self, obj):
        return 0


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'target_user', 'target_message', 'reason', 'description']

    def create(self, validated_data):
        validated_data['reporter'] = self.context['request'].user
        return super().create(validated_data)
