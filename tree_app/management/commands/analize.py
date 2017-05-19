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
        data_file = os.path.join(report_path, "stat.csv")
        self.stdout.write("Exporting statistics table")
        export_csv(data_file, summary_statistics_table)
        self.stdout.write("Export success!")


def collect_statistics():
    summary_statistics_table = []

    types = {
        "ltree": Ltree,
        "raw": Raw,
        "mptt": Mptt
    }

    for k, v in types.iteritems():
        print "Getting {} operations statistics".format(k)
        summary_statistics_table += [
            {
                "avg_time": statistics.get_avg_time_full_tree(v),
                "type": k,
                "operation": "read_tree"
            },
            {
                "avg_time": statistics.get_avg_time_sub_tree(v),
                "type": k,
                "operation": "read_node"
            },
            {
                "avg_time": statistics.get_avg_time_add_node(v),
                "type": k,
                "operation": "add_node"
            },
            {
                "avg_time": statistics.get_avg_time_move_node(v),
                "type": k,
                "operation": "move_node"
            }
        ]
    return summary_statistics_table


def export_csv(data_file, data):
    with open(data_file, "wb") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["avg_time", "type", "operation"])
        writer.writeheader()
        writer.writerows(data)
