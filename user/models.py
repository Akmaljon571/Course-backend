from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from region.models import RegionModel


class CustomUser(AbstractUser):
    region = models.ForeignKey(RegionModel, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(limit_value=10), MaxValueValidator(limit_value=100)],
    )
    phone = models.CharField(max_length=12)
    avatar = models.ImageField(upload_to='avatar/')
    discount = models.PositiveIntegerField(
        validators=[MaxValueValidator(limit_value=100)],
        default=0
    )

    def __str__(self):
        return self.username
