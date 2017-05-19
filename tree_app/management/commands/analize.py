# coding=utf-8
# -*- coding: utf-8 -*-
import csv
import os
from django.core.management import BaseCommand
from tree_app.models import Raw, Mptt, Ltree
from tree_app import statistics


class Command(BaseCommand):
    # Show this when the user types help
    help = "Tree statistics"

    def handle(self, *args, **options):
        report_path = "./report"
        if not os.path.exists(report_path):
            os.makedirs(report_path)

        # собираем статистику
        summary_statistics_table = collect_statistics()

        # экспорт данных
        self.stdout.write("Exporting statistics table")
        data_file = os.path.join(report_path, "stat.csv")

        with open(data_file, "wb") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=["avg_time", "type", "operation"])
            writer.writeheader()
            writer.writerows(summary_statistics_table)

        self.stdout.write("Export success!")


def collect_statistics():
    summary_statistics_table = []

    types = {
        "ltree": Ltree,
        "raw": Raw,
        "mptt": Mptt
    }

    # 1. чтение всего дерева
    print "Get read tree statistics"
    operation = "read_tree"
    for k, v in types.iteritems():
        summary_statistics_table.append(
            {
                "avg_time": statistics.get_avg_time_full_tree(v),
                "type": k,
                "operation": operation
            }
        )

    # 2. Чтение произвольного узла
    print "Get read node statistics"
    operation = "read_subtree"
    # т.к. самый массивный из 12 уровней
    node_id = 8
    for k, v in types.iteritems():
        summary_statistics_table.append(
            {
                "avg_time": statistics.get_avg_time_sub_tree(v, node_id),
                "type": k,
                "operation": operation
            }
        )

    # 3. Перемещение поддерева
    print "Get move footer node to top statistics"
    operation = "move_subtree"
    target_node_id = 2
    moved_node_id = 29654
    for k, v in types.iteritems():
        summary_statistics_table.append(
            {
                "avg_time": statistics.get_avg_time_move_node(v, target_node_id, moved_node_id),
                "type": k,
                "operation": operation
            }
        )

    # 4. Вставка узла
    print "Get append node statistics"
    target_node_id = 19893
    operation = "add_node"
    for k, v in types.iteritems():
        summary_statistics_table.append(
            {
                "avg_time": statistics.get_avg_time_add_node(v, target_node_id),
                "type": k,
                "operation": operation
            }
        )

    return summary_statistics_table
