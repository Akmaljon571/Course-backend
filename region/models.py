from django.db import models


class RegionModel(models.Model):
    title = models.CharField(max_length=255, unique=True)
    soato = models.IntegerField()

    def __str__(self):
        return self.title
