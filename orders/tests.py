from django.core.management import call_command
from django.test import TestCase
from types import SimpleNamespace
from .models import Box, Order, OrderItem, Product
from .packing import Item, fits_box, recommend_box


class PackingTests(TestCase):
    def test_rotation_allows_item_to_fit(self):
        self.assertTrue(fits_box([Item((11, 4, 3), 1)], type("B", (), {"dimensions": (4, 12, 4), "max_weight": 2})()))

    def test_rejects_weight_over_capacity(self):
        self.assertFalse(fits_box([Item((2, 2, 2), 3)], type("B", (), {"dimensions": (10, 10, 10), "max_weight": 2})()))

    def test_rejects_item_that_exceeds_box_dimensions(self):
        self.assertFalse(fits_box([Item((12, 2, 2), 1)], type("B", (), {"dimensions": (10, 10, 10), "max_weight": 5})()))

    def test_places_multiple_items_without_overlap(self):
        items = [Item((6, 5, 5), 1), Item((6, 5, 5), 1)]
        box = type("B", (), {"dimensions": (12, 10, 5), "max_weight": 5})()
        self.assertTrue(fits_box(items, box))

    def test_repeated_items_fit_in_a_simple_grid(self):
        items = [Item((10, 10, 12), 0.45, 7)]
        box = type("B", (), {"dimensions": (36, 28, 20), "max_weight": 8})()
        self.assertTrue(fits_box(items, box))

    def test_recommends_lowest_cost_fitting_box(self):
        product = Product.objects.create(sku="P1", name="Part", length=5, width=5, height=5, weight=1)
        order = Order.objects.create()
        line = OrderItem.objects.create(order=order, product=product, quantity=1)
        too_small = Box.objects.create(name="Tiny", length=3, width=3, height=3, max_weight=5, cost=0.1)
        costly = Box.objects.create(name="Large", length=10, width=10, height=10, max_weight=5, cost=2)
        economical = Box.objects.create(name="Small", length=6, width=6, height=6, max_weight=5, cost=1)
        self.assertNotEqual(too_small, recommend_box([line], Box.objects.all()))
        self.assertEqual(economical, recommend_box([line], [costly, too_small, economical]))


class OrderFlowTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(sku="MUG-01", name="Mug", length=10, width=10, height=10, weight=1)
        Box.objects.create(name="Small", length=20, width=12, height=12, max_weight=5, cost=1)

    def test_home_creates_order_and_shows_recommendation(self):
        response = self.client.post("/", {"items": "MUG-01, 2"})
        self.assertEqual(response.status_code, 302)
        order = Order.objects.get()
        self.assertEqual(order.items.get().quantity, 2)
        self.assertEqual(order.recommended_box.name, "Small")
        detail = self.client.get(response.url)
        self.assertContains(detail, "Recommended box: Small")
        self.assertContains(detail, "2 items")
        self.assertContains(detail, "2.00 kg combined product weight")

    def test_unknown_sku_is_rejected_without_creating_order(self):
        response = self.client.post("/", {"items": "NOPE, 1"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "unknown SKU NOPE")
        self.assertEqual(Order.objects.count(), 0)

    def test_order_without_a_fitting_box_is_saved_with_explanation(self):
        response = self.client.post("/", {"items": "MUG-01, 20"})
        self.assertEqual(response.status_code, 302)
        order = Order.objects.get()
        self.assertIsNone(order.recommended_box)
        self.assertIn("No available box", order.recommendation_note)


class DemoCatalogTests(TestCase):
    def test_seed_demo_provides_ten_products_and_three_boxes(self):
        call_command("seed_demo", verbosity=0)
        self.assertEqual(Product.objects.count(), 10)
        self.assertEqual(Box.objects.count(), 3)
        bottle = Product.objects.get(sku="BOTTLE-02")
        self.assertEqual((bottle.length, bottle.width, bottle.height), (8, 8, 26))
        self.assertEqual(bottle.weight, 0.50)

    def test_order_quantity_can_change_recommended_box(self):
        call_command("seed_demo", verbosity=0)
        product = Product.objects.get(sku="MUG-01")
        boxes = list(Box.objects.all())
        two_mugs = recommend_box([SimpleNamespace(product=product, quantity=2)], boxes)
        five_mugs = recommend_box([SimpleNamespace(product=product, quantity=5)], boxes)
        self.assertEqual(two_mugs.name, "Small")
        self.assertEqual(five_mugs.name, "Medium")
