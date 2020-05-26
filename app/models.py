from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from taxiapp import settings
from django.shortcuts import reverse


class User(AbstractUser):
    """
    We are using Django built in user with Abstract Base user
    for designing application with requirements
    """
    pass


class Trip(models.Model):
    """
    Trip model
    """
    REQUESTED = 'REQUESTED'
    STARTED = 'STARTED'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    STATUSES = (
        (REQUESTED, REQUESTED),
        (STARTED, STARTED),
        (IN_PROGRESS, IN_PROGRESS),
        (COMPLETED, COMPLETED),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    pick_up_address = models.CharField(max_length=255)
    drop_off_address = models.CharField(max_length=255)
    rider = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.DO_NOTHING,
                              related_name="trips_as_rider")
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.DO_NOTHING,
                               related_name="trips_as_driver")
    status = models.CharField(
        max_length=100, choices=STATUSES, default=REQUESTED
    )

    def __str__(self):
        """
        string representation
        :return:
        """
        return "{}".format(self.id)

    def get_absolute_url(self):
        return reverse('trip_detail', kwargs={'trip_id': self.id})
