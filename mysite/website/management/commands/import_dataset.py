import csv
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from website.models import Equipment, EquipmentCategory, Location


STATUS_MAP = {
    "available": Equipment.Status.AVAILABLE,
    "unavailable": Equipment.Status.UNAVAILABLE,
}


class Command(BaseCommand):
    help = "Import Equipment from CSV."

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            type=str,
            default=None,
            help="Optional absolute/relative path to CSV. If omitted, uses website/equipmentDataset.csv",
        )
        parser.add_argument(
            "--update",
            action="store_true",
            help="Update existing equipment (matched by name).",
        )

    @transaction.atomic
    def handle(self, *args, **opts):
        # If user didn't pass --path, use: <BASE_DIR>/website/equipmentDataset.csv
        if opts["path"]:
            csv_path = Path(opts["path"])
        else:
            csv_path = Path(settings.BASE_DIR) / "website" / "equipmentDataset.csv"

        if not csv_path.exists():
            raise CommandError(f"CSV not found: {csv_path}")

        with csv_path.open(newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            required = {"name", "status", "description", "category_name", "location_name", "quantity"}
            missing = required - set(reader.fieldnames or [])
            if missing:
                raise CommandError(f"Missing columns: {sorted(missing)}")

            # Cache existing categories/locations
            cat_cache = {c.name: c for c in EquipmentCategory.objects.all()}
            loc_cache = {l.name: l for l in Location.objects.all()}

            created = updated = skipped = 0

            for line_no, row in enumerate(reader, start=2):
                name = (row["name"] or "").strip()
                if not name:
                    raise CommandError(f"Row {line_no}: blank name")

                raw_status = (row["status"] or "").strip().lower()
                status = STATUS_MAP.get(raw_status)
                if status is None:
                    raise CommandError(
                        f"Row {line_no}: invalid status '{row['status']}'. "
                        f"Use: {', '.join(STATUS_MAP.keys())}"
                    )

                cat_name = (row["category_name"] or "").strip()
                loc_name = (row["location_name"] or "").strip()
                if not cat_name:
                    raise CommandError(f"Row {line_no}: blank category_name")
                if not loc_name:
                    raise CommandError(f"Row {line_no}: blank location_name")

                try:
                    quantity = int(row["quantity"])
                    if quantity < 0:
                        raise ValueError
                except ValueError:
                    raise CommandError(f"Row {line_no}: invalid quantity '{row['quantity']}'")

                category = cat_cache.get(cat_name)
                if category is None:
                    category = EquipmentCategory.objects.create(name=cat_name)
                    cat_cache[cat_name] = category

                location = loc_cache.get(loc_name)
                if location is None:
                    # Your Location fields are optional now, so name-only is fine
                    location = Location.objects.create(name=loc_name)
                    loc_cache[loc_name] = location

                defaults = {
                    "status": status,
                    "description": (row["description"] or "").strip(),
                    "category": category,
                    "location": location,
                    "quantity": quantity,
                }

                if opts["update"]:
                    _, was_created = Equipment.objects.update_or_create(name=name, defaults=defaults)
                    created += int(was_created)
                    updated += int(not was_created)
                else:
                    _, was_created = Equipment.objects.get_or_create(name=name, defaults=defaults)
                    if was_created:
                        created += 1
                    else:
                        skipped += 1

        self.stdout.write(self.style.SUCCESS("Import complete."))
        if opts["update"]:
            self.stdout.write(f"Created: {created}, Updated: {updated}")
        else:
            self.stdout.write(f"Created: {created}, Skipped existing: {skipped}")
