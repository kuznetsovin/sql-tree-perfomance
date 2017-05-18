# -*- coding: utf-8 -*-
import csv
import os
from django.core.management import BaseCommand
from tree_app.models import Raw, Mptt, Ltree


class Command(BaseCommand):
    # Show this when the user types help
    help = "Init test tree tables"

    def add_arguments(self, parser):
        parser.add_argument('init_data_path', type=str)

    def handle(self, *args, **options):
        success_recs = []
        deffer_recs = []
        prev_record_ids = []

        self.stdout.write("Prepair load data")
        # упорядочиваем записи, чтобы не было рассогласования id
        # например когда parent_id появляется раньше созданого id
        with open(options["init_data_path"]) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row["parent_id"] == '':
                    row["parent_id"] = None

                if not prev_record_ids or row["parent_id"] in prev_record_ids:
                    success_recs.append(row)
                    prev_record_ids.append(row["id"])
                else:
                    deffer_recs.append(row)

        self.stdout.write("Loading data")
        map(load_rec, success_recs + deffer_recs)

        self.stdout.write("Tree load success")


def load_rec(data):
    Raw.objects.create(**data)
    Mptt.objects.create(**data)

    if data["parent_id"]:
        prev_node = Ltree.objects.get(id=data["parent_id"])
        node_path = "{}.{}".format(prev_node.path, data["id"])
    else:
        node_path = str(data["id"])

    Ltree.objects.create(
        id=data["id"],
        path=node_path,
        type=data["type"]
    )
