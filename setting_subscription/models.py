import uuid
from django.db import models
from django.utils import timezone
from extensions.utils import jalali_converter

# Create your models here.

"""
start class subscription
"""


class Subscription(models.Model):
    name = models.CharField(max_length=200, verbose_name="عنوان اشتراک")
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(verbose_name="توضیحات اشتراک")
    price = models.BigIntegerField(default=0, verbose_name="قیمت اشتراک", help_text="قیمت براساس ریال می باشد")
    time = models.IntegerField(null=False, blank=False, default=0, verbose_name="مدت زمان اشتراک", help_text="مدت براساس روز می باشد ")
    discount = models.DecimalField(default=0, decimal_places=0, max_digits=2, verbose_name="تخفیف",
                                   help_text="(%) تخفیف براساس درصد می باشد ")
    publish = models.DateTimeField(default=timezone.now, verbose_name="زمان انتشار اشتراک")
    created = models.DateTimeField(auto_now=True)
    update = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False, verbose_name="وضعیت نمایش اشتراک")

    def __str__(self):
        return self.name

    class Meta():
        verbose_name = "اشتراک "
        verbose_name_plural = " اشتراک ها "

    def description_sub(self):
        if len(self.description) > 50:
            return self.description[0:50] + '...'
        else:
            return self.description

    description_sub.short_description = 'توضیحات اشتراک'

    def offer(self):
        if self.discount > 0:
            return int(((100 - self.discount)/100)* self.price)

    def jpublish(self):
        return jalali_converter(self.publish)
    jpublish.short_description = "انتشار"


"""
end class subscription
"""

"""
start class ipAddress
"""


class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name='ادرس ای پی')

    def __str__(self):
        return self.ip_address

    class Meta():
        verbose_name = 'ادرس ای پی'
        verbose_name_plural = 'ادرس ای پی'


"""
end class ipAddress
"""