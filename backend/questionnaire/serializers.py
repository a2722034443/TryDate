from rest_framework import serializers
from .models import Questionnaire


class QuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionnaire
        fields = ['answers', 'completion_rate', 'updated_at']
        read_only_fields = ['completion_rate', 'updated_at']

    def update(self, instance, validated_data):
        new_answers = validated_data.get('answers', {})
        instance.answers.update(new_answers)
        instance.save()
        return instance
