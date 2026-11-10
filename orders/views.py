from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from .forms import OrderRequestForm
from .models import Box, Order, OrderItem, Product
from .packing import recommend_box


def home(request):
    form = OrderRequestForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            order = Order.objects.create()
            order_items = [OrderItem(order=order, product=product, quantity=quantity)
                           for product, quantity in form.cleaned_data["items"]]
            OrderItem.objects.bulk_create(order_items)
            box = recommend_box(order.items.select_related("product").all(), Box.objects.all())
            if box:
                order.recommended_box = box
                order.recommendation_note = f"Recommended the lowest-cost box that fits ({box.cost:.2f})."
            else:
                order.recommendation_note = "No available box can fit this order within its size and weight limits."
            order.save()
        return redirect("order_detail", pk=order.pk)
    return render(request, "orders/home.html", {
        "form": form,
        "orders": Order.objects.prefetch_related("items__product")[:8],
        "product_count": Product.objects.count(),
        "box_count": Box.objects.count(),
    })


def order_detail(request, pk):
    order = get_object_or_404(Order.objects.prefetch_related("items__product"), pk=pk)
    lines = list(order.items.all())
    return render(request, "orders/order_detail.html", {
        "order": order,
        "order_items": [{"item": line, "line_weight": line.product.weight * line.quantity} for line in lines],
        "total_units": sum(line.quantity for line in lines),
        "total_weight": sum(line.product.weight * line.quantity for line in lines),
    })
