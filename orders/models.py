from django.core.validators import MinValueValidator
from django.db import models


class Product(models.Model):
    sku = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=120)
    length = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    width = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    height = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    weight = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])

    class Meta:
        ordering = ["sku"]

    def __str__(self):
        return f"{self.sku} — {self.name}"


class Box(models.Model):
    name = models.CharField(max_length=80, unique=True)
    length = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    width = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    height = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    max_weight = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    cost = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])

    class Meta:
        ordering = ["cost", "name"]

    def __str__(self):
        return self.name


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    recommended_box = models.ForeignKey(Box, null=True, blank=True, on_delete=models.SET_NULL)
    recommendation_note = models.CharField(max_length=240, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.pk}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        constraints = [models.UniqueConstraint(fields=["order", "product"], name="one_line_per_product")]

    def __str__(self):
        return f"{self.product.sku} × {self.quantity}"
