import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email=None, phone=None, password=None, **extra_fields):
        if not email and not phone:
            raise ValueError('邮箱或手机号至少填写一项')
        if email:
            email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email=email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class Gender(models.TextChoices):
        MALE = 'male', '男'
        FEMALE = 'female', '女'
        OTHER = 'other', '其他'

    class GenderPreference(models.TextChoices):
        MALE = 'male', '男'
        FEMALE = 'female', '女'
        BOTH = 'both', '不限'

    class Grade(models.TextChoices):
        FRESHMAN = 'freshman', '大一'
        SOPHOMORE = 'sophomore', '大二'
        JUNIOR = 'junior', '大三'
        SENIOR = 'senior', '大四'
        MASTER1 = 'master1', '研一'
        MASTER2 = 'master2', '研二'
        MASTER3 = 'master3', '研三'
        PHD = 'phd', '博士'

    class CollegeDirection(models.TextChoices):
        STEM = 'stem', '理工'
        HUMANITIES = 'humanities', '文史'
        ART = 'art', '艺术设计'
        BUSINESS = 'business', '经管'
        MEDICINE = 'medicine', '医学'
        OTHER = 'other', '其他'

    class Status(models.TextChoices):
        ACTIVE = 'active', '正常'
        BANNED = 'banned', '封禁'
        DELETED = 'deleted', '注销'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    nickname = models.CharField(max_length=30)
    gender = models.CharField(max_length=10, choices=Gender.choices, default=Gender.MALE)
    gender_preference = models.CharField(max_length=10, choices=GenderPreference.choices, default=GenderPreference.FEMALE)
    birth_year = models.PositiveSmallIntegerField(null=True, blank=True)
    grade = models.CharField(max_length=20, choices=Grade.choices, null=True, blank=True)
    college_direction = models.CharField(max_length=20, choices=CollegeDirection.choices, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.CharField(max_length=50, blank=True, default='')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    questionnaire_completion = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.nickname or str(self.id)

    @property
    def is_eligible_for_matching(self):
        return self.questionnaire_completion >= 70 and self.status == self.Status.ACTIVE


class BlackList(models.Model):
    blocker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocking')
    blocked = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('blocker', 'blocked')
        verbose_name = '黑名单'

    def __str__(self):
        return f'{self.blocker} 屏蔽了 {self.blocked}'


class VerificationCode(models.Model):
    class CodeType(models.TextChoices):
        EMAIL = 'email', '邮箱验证'
        PHONE = 'phone', '手机验证'

    target = models.CharField(max_length=100)
    code = models.CharField(max_length=6)
    code_type = models.CharField(max_length=10, choices=CodeType.choices)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '验证码'

    def __str__(self):
        return f'{self.target} - {self.code}'

