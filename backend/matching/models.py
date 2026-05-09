from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class Match(models.Model):
    class Action(models.TextChoices):
        PENDING = 'pending', '等待'
        LIKED = 'liked', '心动'
        PASSED = 'passed', '再想想'

    class MatchStatus(models.TextChoices):
        PENDING = 'pending', '等待双方确认'
        MATCHED = 'matched', '双向心动'
        MISSED = 'missed', '已错过'

    user_a = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='matches_as_a'
    )
    user_b = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='matches_as_b'
    )
    compatibility_score = models.FloatField(default=0.0)
    dimension_scores = models.JSONField(default=dict)
    compatibility_highlights = models.JSONField(default=list)
    user_a_action = models.CharField(max_length=10, choices=Action.choices, default=Action.PENDING)
    user_b_action = models.CharField(max_length=10, choices=Action.choices, default=Action.PENDING)
    status = models.CharField(max_length=10, choices=MatchStatus.choices, default=MatchStatus.PENDING)
    week_number = models.CharField(max_length=10)
    matched_at = models.DateTimeField(auto_now_add=True)
    action_deadline = models.DateTimeField()

    class Meta:
        verbose_name = '匹配'
        verbose_name_plural = '匹配'
        unique_together = ('user_a', 'user_b', 'week_number')

    def save(self, *args, **kwargs):
        if not self.action_deadline:
            self.action_deadline = timezone.now() + timedelta(hours=48)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Week {self.week_number}: {self.user_a} ↔ {self.user_b} [{self.status}]'

    def get_action_for(self, user):
        if user == self.user_a:
            return self.user_a_action
        return self.user_b_action

    def set_action_for(self, user, action):
        if user == self.user_a:
            self.user_a_action = action
        else:
            self.user_b_action = action
        if self.user_a_action == self.Action.LIKED and self.user_b_action == self.Action.LIKED:
            self.status = self.MatchStatus.MATCHED
        elif self.Action.PASSED in (self.user_a_action, self.user_b_action):
            self.status = self.MatchStatus.MISSED
        self.save()

