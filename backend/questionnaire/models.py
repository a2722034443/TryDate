from django.db import models
from django.conf import settings


TOTAL_QUESTIONS = 10


class Questionnaire(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='questionnaire',
    )
    answers = models.JSONField(default=dict)
    completion_rate = models.PositiveSmallIntegerField(default=0)
    last_modified_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '问卷'
        verbose_name_plural = '问卷'

    def __str__(self):
        return f'{self.user.nickname} 的问卷（{self.completion_rate}%）'

    def calculate_completion(self):
        answered = len([v for v in self.answers.values() if v is not None and v != '' and v != []])
        rate = int(answered / TOTAL_QUESTIONS * 100)
        self.completion_rate = min(rate, 100)
        return self.completion_rate

    def save(self, *args, **kwargs):
        self.calculate_completion()
        super().save(*args, **kwargs)
        self.user.questionnaire_completion = self.completion_rate
        self.user.save(update_fields=['questionnaire_completion'])

