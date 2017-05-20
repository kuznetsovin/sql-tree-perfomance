# coding=utf-8
import random

from django.db import connection, reset_queries
from django.conf import settings
from pandas import DataFrame

from tree_app.models import Raw, Mptt, Ltree

settings.DEBUG = True

MODEL_FIELD = "model"
OPERATION_FIELD = "operation"
TIME_FIELD = "time"


def read_tree_time(model):
    # т.к. используется "ленивая" модель запросов, то чтобы запрос отправиля в базу
    # он преобразуется в список
    list(model.objects.all())

    result = {
        MODEL_FIELD: model.__name__,
        OPERATION_FIELD: "read_tree",
        TIME_FIELD: float(connection.queries[0]["time"])
    }
    reset_queries()

    return result


def read_node_time(model):
    all_nodes = list(model.objects.all())
    reset_queries()

    node = random.choice(all_nodes)
    # т.к. используется "ленивая" модель запросов, то чтобы запрос отправиля в
    # базу он преобразуется в список
    list(node.get_descendants(include_self=True))

    result = {
        MODEL_FIELD: model.__name__,
        OPERATION_FIELD: "read_node",
        TIME_FIELD: float(connection.queries[0]["time"])
    }
    reset_queries()

    return result


def move_node_time(model):
    all_nodes = list(model.objects.all())
    reset_queries()

    parent_node = random.choice(all_nodes)
    moved_node = random.choice(all_nodes)

    moved_node.move_to(parent_node)

    result = {
        MODEL_FIELD: model.__name__,
        OPERATION_FIELD: "move_node",
        TIME_FIELD: float(connection.queries[0]["time"])
    }
    reset_queries()

    return result


def insert_node_time(model):
    all_nodes = list(model.objects.all())
    reset_queries()

    if model.__name__ == "Ltree":
        target_node = random.choice(all_nodes)

        new_node = model.objects.create(path=target_node.path, type="company")
        new_node.path += ".{}".format(new_node.id)
        new_node.save()

        time = sum([float(r["time"]) for r in connection.queries])
    else:
        target_node = random.choice(all_nodes)
        model.objects.create(parent=target_node, type="company")
        time = float(connection.queries[0]["time"])

    result = {
        MODEL_FIELD: model.__name__,
        OPERATION_FIELD: "insert_node",
        TIME_FIELD: time
    }
    reset_queries()

    return result


def collect_statistics(iter_count):
    summary_statistics_table = []

    models = [Ltree, Raw, Mptt]

    for m in models:
        print "Read time for {} model".format(m.__name__)
        for i in xrange(iter_count):
            print "Iteration: {}".format(i)
            summary_statistics_table += [
                read_tree_time(m),
                read_node_time(m),
                move_node_time(m),
                insert_node_time(m)
            ]

    result = DataFrame(
        data=summary_statistics_table
    )
    return result
