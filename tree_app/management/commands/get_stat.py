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

    def add_arguments(self, parser):
        parser.add_argument('result_file', type=str)

    def handle(self, *args, **options):
        summary_statistics_table = []

        types = {
            "ltree": Ltree,
            "raw": Raw,
            "mptt": Mptt
        }

        # 1. чтение всего дерева
        self.stdout.write("Get read tree statistics")
        operation = "read_tree"
        for k,v in types.iteritems():
            summary_statistics_table.append(
                {
                    "avg_time": statistics.get_avg_time_full_tree(v),
                    "type": k,
                    "operation": operation
                }
            )
        # 2. Чтение произвольного узла
        self.stdout.write("Get read node statistics")
        operation = "read_sub_tree"
        # т.к. самый массивный из 12 уровней
        node_id = 8
        for k,v in types.iteritems():
            summary_statistics_table.append(
                {
                    "avg_time": statistics.get_avg_time_sub_tree(v, node_id),
                    "type": k,
                    "operation": operation
                }
            )

        # 3. Перемещение узла с нижнего на верхний уровень
        self.stdout.write("Get move footer node to top statistics")
        operation = "footer_top_move"
        for k,v in types.iteritems():
            summary_statistics_table.append(
                {
                    "avg_time": statistics.get_avg_time_move_footer_node_to_top(v),
                    "type": k,
                    "operation": operation
                }
            )

        # 4. Перемещение узла внутри уровня
        self.stdout.write("Get move one level nodes statistics")
        operation = "one_level_move"
        for k,v in types.iteritems():
            summary_statistics_table.append(
                {
                    "avg_time": statistics.get_avg_time_move_one_level_nodes(v),
                    "type": k,
                    "operation": operation
                }
            )

        # 5. Вставка узла на второй уровень
        self.stdout.write("Get append node statistics")
        operation = "add_tree"
        for k,v in types.iteritems():
            summary_statistics_table.append(
                {
                    "avg_time": statistics.get_avg_time_add_node(v),
                    "type": k,
                    "operation": operation
                }
            )

        # экспорт данных
        self.stdout.write("Exporting statistics table")
        with open(options["result_file"], "wb") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=["avg_time", "type", "operation"])
            writer.writeheader()
            writer.writerows(summary_statistics_table)

        self.stdout.write("Export success!")