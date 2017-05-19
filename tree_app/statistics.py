# coding=utf-8
import random

from django.db import connection, reset_queries
from django.conf import settings

settings.DEBUG = True

COUNT_ITER = 100


def get_avg_time_full_tree(model, count_iter=COUNT_ITER):
    # т.к. используется "ленивая" модель запросов, то чтобы запрос отправиля в базу
    # он преобразуется в список
    for i in xrange(count_iter): list(model.objects.all());

    times = [float(r["time"]) for r in connection.queries]
    reset_queries()

    result = sum(times) / len(times)
    return result


def get_avg_time_sub_tree(model, count_iter=COUNT_ITER):
    all_nodes = list(model.objects.all())
    reset_queries()

    for i in xrange(count_iter):
        node = random.choice(all_nodes)
        # т.к. используется "ленивая" модель запросов, то чтобы запрос отправиля в базу
        # он преобразуется в список
        list(node.get_descendants())

    times = [float(r["time"]) for r in connection.queries]

    result = sum(times) / len(times)
    return result


def get_avg_time_move_node(model, count_iter=COUNT_ITER):
    all_nodes = list(model.objects.all())
    reset_queries()

    for i in xrange(count_iter):
        parent_node = random.choice(all_nodes)
        moved_node = random.choice(all_nodes)

        moved_node.move_to(parent_node)

    times = [float(r["time"]) for r in connection.queries]
    result = sum(times) / len(times)
    return result


def get_avg_time_add_node(model, count_iter=COUNT_ITER):
    all_nodes = list(model.objects.all())
    reset_queries()
    times = []

    if model.__name__ == "Ltree":
        for i in xrange(count_iter):
            target_node = random.choice(all_nodes)

            new_node = model.objects.create(path=target_node.path, type="company")
            new_node.path += ".{}".format(new_node.id)
            new_node.save()
            times.append(sum([float(r["time"]) for r in connection.queries]))
            reset_queries()
    else:
        for i in xrange(count_iter):
            target_node = random.choice(all_nodes)
            model.objects.create(parent=target_node, type="company")
        times = [float(r["time"]) for r in connection.queries]

    result = sum(times) / len(times)
    return result
