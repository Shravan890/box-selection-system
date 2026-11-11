from django.core.management.base import BaseCommand
from orders.models import Box, Product


class Command(BaseCommand):
    help = "Add a small editable catalog for trying the box recommender."

    def handle(self, *args, **options):
        products = [
            ("MUG-01", "Ceramic mug", 10, 10, 12, 0.45),
            ("BOOK-01", "Hardcover book", 21, 15, 3, 0.65),
            ("LAMP-01", "Desk lamp", 28, 18, 12, 1.8),
            ("BOTTLE-02", "Reusable water bottle", 8, 8, 26, 0.50),
            ("HEADPHONES-01", "Over-ear headphones", 20, 18, 8, 0.35),
            ("SNEAKER-01", "Running shoe pair", 32, 22, 12, 1.10),
            ("PHONE-01", "Smartphone", 16, 8, 2, 0.22),
            ("TOY-01", "Building block set", 24, 16, 10, 0.75),
            ("CANDLE-01", "Glass jar candle", 9, 9, 11, 0.40),
            ("KETTLE-01", "Electric kettle", 24, 20, 22, 1.30),
        ]
        boxes = [
            ("Small", 24, 20, 16, 3, 1.25),
            ("Medium", 36, 28, 20, 8, 2.10),
            ("Large", 48, 36, 30, 15, 3.40),
        ]
        for sku, name, length, width, height, weight in products:
            Product.objects.get_or_create(sku=sku, defaults={
                "name": name, "length": length, "width": width, "height": height, "weight": weight,
            })
        for name, length, width, height, max_weight, cost in boxes:
            Box.objects.get_or_create(name=name, defaults={
                "length": length, "width": width, "height": height,
                "max_weight": max_weight, "cost": cost,
            })
        self.stdout.write(self.style.SUCCESS("Demo catalog is ready: 10 products and 3 boxes."))
