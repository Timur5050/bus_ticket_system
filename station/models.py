from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint

from user.models import User


class Facility(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'Facilities'

    def __str__(self):
        return str(self.name)


class Bus(models.Model):
    info = models.CharField(max_length=255, null=True, blank=True)
    num_seats = models.IntegerField()
    facilities = models.ManyToManyField(Facility, related_name='buses')

    class Meta:
        verbose_name_plural = "buses"

    def __str__(self):
        return f"Bus: {self.info} (id = {self.id})"


class Trip(models.Model):
    source = models.CharField(max_length=63)
    destination = models.CharField(max_length=63)
    departure = models.DateTimeField()
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['source', 'destination']),
            models.Index(fields=['departure']),
        ]

    def __str__(self):
        return f"{self.source} - {self.destination} ({self.departure})"


class Ticket(models.Model):
    seat = models.IntegerField()
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="tickets")
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="tickets")

    class Meta:
        constraints = [
            UniqueConstraint(fields=['trip', 'order'], name='unique_ticket'),
        ]

    def __str__(self):
        return f"{self.trip} - (seat - {self.seat})"

    def clean(self):
        if not (1 <= self.seat <= self.trip.bus.num_seats):
            raise ValueError({
                "seat": f"seat must be in range (1, {self.trip.bus.num_seats})"
            })

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None
    ):
        self.full_clean()
        return super(Ticket, self).save(force_insert, force_update, using, update_fields)


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.created_at)
