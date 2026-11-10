from django import forms
from .models import Product


class OrderRequestForm(forms.Form):
    items = forms.CharField(
        label="Order items",
        widget=forms.Textarea(attrs={"rows": 5, "placeholder": "MUG-01, 2\nBOOK-01, 1"}),
        help_text="Enter one SKU and quantity per line, separated by a comma.",
    )

    def clean_items(self):
        raw = self.cleaned_data["items"]
        lines = []
        seen = set()
        errors = []
        for number, line in enumerate(raw.splitlines(), 1):
            if not line.strip():
                continue
            parts = [part.strip() for part in line.split(",")]
            if len(parts) != 2:
                errors.append(f"Line {number}: use SKU, quantity.")
                continue
            sku, quantity_text = parts
            if sku in seen:
                errors.append(f"Line {number}: SKU {sku} appears more than once.")
                continue
            seen.add(sku)
            try:
                quantity = int(quantity_text)
                if quantity < 1:
                    raise ValueError
            except ValueError:
                errors.append(f"Line {number}: quantity must be a positive whole number.")
                continue
            try:
                product = Product.objects.get(sku__iexact=sku)
            except Product.DoesNotExist:
                errors.append(f"Line {number}: unknown SKU {sku}.")
                continue
            lines.append((product, quantity))
        if not lines and not errors:
            errors.append("Enter at least one order item.")
        if errors:
            raise forms.ValidationError(errors)
        return lines
