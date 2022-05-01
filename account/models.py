from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
from setting_subscription.models import Subscription
from extensions.utils import jalali_converter
from PIL import Image


# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='ایمیل')
    is_author = models.BooleanField(default=False, verbose_name='وضعیت نویسندگی')
    image = models.ImageField(blank=True, null=True, verbose_name='تصویر', upload_to='image_user')
    special_user = models.DateTimeField(default=timezone.now, verbose_name="کاربر ویژه")

    def is_special_user(self):
        if self.special_user > timezone.now():
            return True
        else:
            return False

    is_special_user.boolean = True
    is_special_user.short_description = "وضعیت کاربر ویژه "

