# -*- coding: utf-8 -*-

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from ltreefield import LtreeField


class Raw(models.Model):
    """
    Модель для теста рекурсивных запросов.
    """
    parent = models.ForeignKey(
         'self',
         null=True,
         blank=True,
         related_name='children',
         db_index=True
    )
    type = models.CharField(max_length=20)


class Mptt(MPTTModel):
    """
    Модель для теста mptt.
    """

    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        db_index=True
    )
    type = models.CharField(max_length=20)

    class MPTTMeta:
        order_insertion_by = ['id']


class Ltree(models.Model):
    """
    Модель для теста ltree.
    """
    path = LtreeField(max_length=1000)
    type = models.CharField(max_length=20)
