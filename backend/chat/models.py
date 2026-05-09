import uuid
from django.db import models
from django.conf import settings


class ChatRoom(models.Model):
    match = models.OneToOneField(
        'matching.Match', on_delete=models.CASCADE, related_name='chat_room'
    )
    is_active = models.BooleanField(default=True)
    last_message_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '聊天室'

    def __str__(self):
        return f'Room for Match {self.match_id}'

    def get_other_user(self, user):
        m = self.match
        return m.user_b if m.user_a == user else m.user_a


class Message(models.Model):
    class MsgType(models.TextChoices):
        TEXT = 'text', '文字'
        IMAGE = 'image', '图片'
        SYSTEM = 'system', '系统消息'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, related_name='sent_messages'
    )
    msg_type = models.CharField(max_length=10, choices=MsgType.choices, default=MsgType.TEXT)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '消息'
        ordering = ['created_at']

    def __str__(self):
        return f'[{self.msg_type}] {self.sender}: {self.content[:30]}'


class Report(models.Model):
    class Reason(models.TextChoices):
        HARASSMENT = 'harassment', '骚扰/辱骂'
        INAPPROPRIATE = 'inappropriate_content', '不当内容'
        FAKE = 'fake', '虚假信息'
        OTHER = 'other', '其他'

    class ReportStatus(models.TextChoices):
        PENDING = 'pending', '待处理'
        REVIEWED = 'reviewed', '已审核'
        RESOLVED = 'resolved', '已处理'
        DISMISSED = 'dismissed', '已驳回'

    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports_filed'
    )
    target_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports_received'
    )
    target_message = models.ForeignKey(
        Message, on_delete=models.SET_NULL, null=True, blank=True
    )
    reason = models.CharField(max_length=30, choices=Reason.choices)
    description = models.TextField(blank=True, default='')
    status = models.CharField(max_length=10, choices=ReportStatus.choices, default=ReportStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '举报'

    def __str__(self):
        return f'{self.reporter} 举报 {self.target_user}: {self.reason}'

