# coding=utf-8
# -*- coding: utf-8 -*-
from django.core.management import BaseCommand
from tree_app.statistics import collect_statistics, MODEL_FIELD, \
    OPERATION_FIELD, TIME_FIELD
from pandas import DataFrame


class Command(BaseCommand):
    # Show this when the user types help
    help = "Tree statistics"

    def add_arguments(self, parser):
        parser.add_argument('iter_count', type=int)

    def handle(self, *args, **options):
        # собираем статистику
        iter_count = options["iter_count"]
        df = DataFrame(
            data=collect_statistics(iter_count)
        )

        self.stdout.write("Export raw data")
        filename = "report/raw_query_times_{}.csv".format(iter_count)
        df.to_csv(filename, index=False)

        self.stdout.write("Pivot table creating")
        pivot_stat = df.pivot_table(
            values=TIME_FIELD,
            index=MODEL_FIELD,
            columns=OPERATION_FIELD
        )

        filename = "report/pivot_stat_{}.csv".format(iter_count)
        pivot_stat.to_csv(filename)
