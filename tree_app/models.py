# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import F
from django.db.models import Func
from django.db.models import Value
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

    def move_to(self, target):
        self.parent = target
        self.save()


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

    def move_to(self, target):
        params = {
            "new_path": "{}.{}".format(target.path, self.id),
            "old_path": self.path
        }

        sql = """UPDATE tree_app_ltree
                SET path = text2ltree(replace(ltree2text(path), %(old_path)s, %(new_path)s))
                WHERE path <@ %(old_path)s"""
        Ltree.objects.raw(sql, params)
