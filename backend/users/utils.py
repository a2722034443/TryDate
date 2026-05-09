import random
import string
from django.core.mail import send_mail
from django.conf import settings
from .models import VerificationCode


def generate_code(length=6):
    return ''.join(random.choices(string.digits, k=length))


def send_email_code(email: str) -> str:
    code = generate_code()
    VerificationCode.objects.create(target=email, code=code, code_type='email')
    send_mail(
        subject='【DLNUDate】您的验证码',
        message=f'您的验证码是：{code}，{settings.VERIFICATION_CODE_EXPIRE_MINUTES} 分钟内有效。',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
    return code


def send_phone_code(phone: str) -> str:
    code = generate_code()
    VerificationCode.objects.create(target=phone, code=code, code_type='phone')
    # TODO: 接入短信服务商 SDK（如阿里云、腾讯云）
    print(f'[SMS] {phone} 的验证码：{code}')
    return code
