from django.db import models

from livefield import LiveField
from livefield import LiveManager
from livefield import LiveModel


class Item(LiveModel):
    pass


class Person(models.Model):
    name = models.CharField(max_length=20)
    alive = LiveField()

    class Meta:
        unique_together = ('name', 'alive')

    objects = LiveManager()
    all_objects = LiveManager(include_soft_deleted=True)
