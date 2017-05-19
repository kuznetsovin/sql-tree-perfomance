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

    def get_descendants(self, include_self=False):
        sql = """WITH RECURSIVE t AS (
          SELECT * FROM tree_app_raw WHERE id = %s
          UNION
          SELECT tree_app_raw.* FROM tree_app_raw JOIN t ON tree_app_raw.parent_id = t.id
        )
        SELECT * FROM t"""

        if not include_self:
            sql += " OFFSET 1"

        return Raw.objects.raw(sql, [self.id])


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

    def get_descendants(self, include_self=False):
        result = Ltree.objects.filter(path__dore=self.path)
        if not include_self:
            result = result.exclude(id=self.id)

        return result
