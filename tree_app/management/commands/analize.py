# coding=utf-8
# -*- coding: utf-8 -*-
from django.core.management import BaseCommand
from tree_app.statistics import collect_statistics, MODEL_FIELD, \
    OPERATION_FIELD, TIME_FIELD


class Command(BaseCommand):
    # Show this when the user types help
    help = "Tree statistics"

    def add_arguments(self, parser):
        parser.add_argument('iter_count', type=int)

    def handle(self, *args, **options):
        # собираем статистику
        iter_count = options["iter_count"]
        statistics = collect_statistics(iter_count)

        self.stdout.write("Export raw data")
        statistics.to_csv(
            "report/raw_query_times_{}.csv".format(iter_count),
            index=False
        )

        self.stdout.write("Pivot table creating")
        statistics.pivot_table(
            values=TIME_FIELD,
            index=MODEL_FIELD,
            columns=OPERATION_FIELD
        ).to_csv(
            "report/pivot_stat_{}.csv".format(iter_count)
        )
