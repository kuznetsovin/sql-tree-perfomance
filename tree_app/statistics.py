# coding=utf-8
from django.db import connection, reset_queries
from django.conf import settings

settings.DEBUG = True


def get_avg_time_full_tree(model, count_iter=50):
    # т.к. используется "ленивая" модель запросов, то чтобы запрос отправиля в базу
    # он преобразуется в список
    for i in xrange(count_iter): list(model.objects.all());

    times = [float(r["time"]) for r in connection.queries]
    reset_queries()

    # вычисляем среднее время выполнения
    result = sum(times) / len(times)
    return result


def get_avg_time_sub_tree(model, node_id, count_iter=50):
    node = model.objects.get(id=node_id)
    reset_queries()

    # т.к. используется "ленивая" модель запросов, то чтобы запрос отправиля в базу
    # он преобразуется в список
    for i in xrange(count_iter): list(node.get_descendants());

    times = [float(r["time"]) for r in connection.queries]

    # вычисляем среднее время выполнения
    result = sum(times) / len(times)
    return result


def get_avg_time_move_node(model, parent_node_id, moved_node_id):
    parent_node = model.objects.get(id=parent_node_id)
    moved_node = model.objects.get(id=moved_node_id)
    reset_queries()

    moved_node.move_to(parent_node)

    result = float(connection.queries[0]["time"])
    return result


def get_avg_time_add_node(model, parent_node_id):
    target_node = model.objects.get(pk=parent_node_id)
    reset_queries()

    if model.__name__ == "Ltree":
        new_node = model.objects.create(path=target_node.path, type="company")
        new_node.path += ".{}".format(new_node.id)
        new_node.save()
    else:
        model.objects.create(parent_id=parent_node_id, type="company")

    result = sum([float(r["time"]) for r in connection.queries])
    return result