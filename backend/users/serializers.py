import random
import string
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from rest_framework import serializers
from .models import User, VerificationCode


class SendCodeSerializer(serializers.Serializer):
    target = serializers.CharField()
    code_type = serializers.ChoiceField(choices=['email', 'phone'])


class RegisterSerializer(serializers.Serializer):
    target = serializers.CharField()
    code_type = serializers.ChoiceField(choices=['email', 'phone'])
    code = serializers.CharField(max_length=6)
    nickname = serializers.CharField(max_length=30)
    gender = serializers.ChoiceField(choices=User.Gender.choices)
    gender_preference = serializers.ChoiceField(choices=User.GenderPreference.choices)
    birth_year = serializers.IntegerField(min_value=1990, max_value=2010, required=False)

    def validate(self, data):
        expire_time = timezone.now() - timedelta(minutes=settings.VERIFICATION_CODE_EXPIRE_MINUTES)
        vc = VerificationCode.objects.filter(
            target=data['target'],
            code=data['code'],
            code_type=data['code_type'],
            is_used=False,
            created_at__gte=expire_time,
        ).last()
        if not vc:
            raise serializers.ValidationError({'code': '验证码无效或已过期'})
        data['_vc'] = vc
        return data

    def create(self, validated_data):
        vc = validated_data.pop('_vc')
        validated_data.pop('code')
        code_type = validated_data.pop('code_type')
        target = validated_data.pop('target')

        if code_type == 'email':
            user = User.objects.create_user(email=target, password=None, **validated_data)
        else:
            user = User.objects.create_user(phone=target, password=None, **validated_data)

        vc.is_used = True
        vc.save()
        return user


class LoginSerializer(serializers.Serializer):
    target = serializers.CharField()
    code = serializers.CharField(max_length=6)
    code_type = serializers.ChoiceField(choices=['email', 'phone'])

    def validate(self, data):
        expire_time = timezone.now() - timedelta(minutes=settings.VERIFICATION_CODE_EXPIRE_MINUTES)
        vc = VerificationCode.objects.filter(
            target=data['target'],
            code=data['code'],
            code_type=data['code_type'],
            is_used=False,
            created_at__gte=expire_time,
        ).last()
        if not vc:
            raise serializers.ValidationError({'code': '验证码无效或已过期'})

        if data['code_type'] == 'email':
            user = User.objects.filter(email=data['target'], status=User.Status.ACTIVE).first()
        else:
            user = User.objects.filter(phone=data['target'], status=User.Status.ACTIVE).first()

        if not user:
            raise serializers.ValidationError({'target': '账号不存在'})

        data['_vc'] = vc
        data['_user'] = user
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'nickname', 'gender', 'gender_preference', 'birth_year',
            'grade', 'college_direction', 'avatar_url', 'bio',
            'questionnaire_completion', 'created_at',
        ]
        read_only_fields = ['id', 'questionnaire_completion', 'created_at']

    def get_avatar_url(self, obj):
        if obj.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.avatar.url)
        return None


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nickname', 'bio', 'grade', 'college_direction', 'birth_year', 'gender_preference', 'avatar']
