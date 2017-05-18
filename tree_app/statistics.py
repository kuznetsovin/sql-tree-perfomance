# coding=utf-8
from django.db import connection, reset_queries
from django.conf import settings

settings.DEBUG = True


def get_avg_time_full_tree(model, count_iter=50):
    for i in xrange(count_iter): print model.objects.all();
    times = [float(r["time"]) for r in connection.queries]
    reset_queries()

    result = reduce(lambda x, y: x + y, times) / len(times)
    return result


def get_avg_time_sub_tree(model, node):
    result = 0
    return result


def get_avg_time_move_footer_node_to_top(model):
    result = 0
    return result


def get_avg_time_move_one_level_nodes(model):
    result = 0
    return result


def get_avg_time_add_node(model):
    result = 0
    return result
