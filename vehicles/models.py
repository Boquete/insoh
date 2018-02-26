from django.db import models
from django.db.models.signals import pre_save
from django.utils.translation import gettext as _
from django.utils.functional import cached_property


class Vehicle(models.Model):
    vid = models.SlugField(_('Vehicle ID'), unique=True)
    name = models.CharField('Name', max_length=50)

    def __str__(self):
        return self.name

    @cached_property
    def batteries_enabled(self):
        return self.batteries.filter(is_enabled=True).count()

    @cached_property
    def batteries_disabled(self):
        return self.batteries.filtfer(is_enabled=False).count()


class Battery(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='batteries')
    number = models.IntegerField(_('Number'), editable=False)
    bid = models.IntegerField(_('Battery ID'), editable=False)
    is_enabled = models.BooleanField(default=True)

    def __str__(self):
        return 'Number={0}, Battery ID={1}, Vehicle={2}'.format(self.number, self.bid, self.vehicle.name)

    class Meta:
        unique_together = (('number', 'vehicle'), ('bid', 'vehicle'))
        verbose_name_plural = 'batteries'


def create_battery_bid(last):
    if last:
        return last.bid + 2
    else:
        return 5


def create_battery_number(last):
    if last:
        return last.number + 1
    else:
        return 1


def pre_save_project_receiver(sender, instance, *args, **kwargs):
    if not instance.pk:
        last = instance.vehicle.batteries.order_by("bid").last()
        instance.bid = create_battery_bid(last)
        instance.number = create_battery_number(last)


pre_save.connect(pre_save_project_receiver, sender=Battery)
