"""Greedy 3D guillotine packing heuristic used for box recommendations."""
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Item:
    dimensions: tuple[float, float, float]
    weight: float
    quantity: int = 1


def _orientations(dimensions):
    return sorted(set((a, b, c) for a in dimensions for b in dimensions for c in dimensions
                      if sorted((a, b, c)) == sorted(dimensions)), reverse=True)


def fits_box(items, box):
    """Return whether all item copies fit in one box, allowing rotation.

    Free spaces are split into disjoint axis-aligned cuboids after each placement.
    The heuristic is deterministic and rejects weight overflow before attempting packing.
    """
    normalized = []
    total_weight = 0.0
    for item in items:
        dims = tuple(float(value) for value in item.dimensions)
        if len(dims) != 3 or min(dims) <= 0 or item.quantity < 1 or item.weight <= 0:
            return False
        for _ in range(item.quantity):
            normalized.append(dims)
            total_weight += float(item.weight)

    box_dims = tuple(float(value) for value in box.dimensions)
    if len(box_dims) != 3 or total_weight > float(box.max_weight):
        return False
    if any(not any(all(d <= b for d, b in zip(orientation, box_dims))
                   for orientation in _orientations(dims)) for dims in normalized):
        return False

    # A regular grid is a fast, reliable positive check for repeated identical items.
    # It catches common cases where the greedy free-space ordering would use a larger box.
    if normalized and all(dims == normalized[0] for dims in normalized):
        for orientation in _orientations(normalized[0]):
            grid_capacity = 1
            for available, item_size in zip(box_dims, orientation):
                grid_capacity *= int(available // item_size)
            if grid_capacity >= len(normalized):
                return True

    normalized.sort(key=lambda dims: (-dims[0] * dims[1] * dims[2], -max(dims), -sum(dims)))
    free = [box_dims]
    for dims in normalized:
        placed = False
        for space_index, space in enumerate(free):
            for orientation in _orientations(dims):
                if all(d <= s for d, s in zip(orientation, space)):
                    x, y, z = space
                    a, b, c = orientation
                    free.pop(space_index)
                    # These three regions are disjoint and cover the unoccupied remainder.
                    free.extend([(x - a, y, z), (a, y - b, z), (a, b, z - c)])
                    free = [region for region in free if min(region) > 0]
                    free = [region for i, region in enumerate(free)
                            if not any(i != j
                                       and all(v <= w for v, w in zip(region, other))
                                       and (region != other or j < i)
                                       for j, other in enumerate(free))]
                    placed = True
                    break
            if placed:
                break
        if not placed:
            return False
    return True


def recommend_box(order_items, boxes):
    """Choose the lowest-cost fitting box; break ties by internal volume then name."""
    items = [Item(
        (float(line.product.length), float(line.product.width), float(line.product.height)),
        float(line.product.weight), line.quantity,
    ) for line in order_items]
    candidates = sorted(boxes, key=lambda box: (
        Decimal(box.cost), Decimal(box.length) * Decimal(box.width) * Decimal(box.height), box.name
    ))
    return next((box for box in candidates if fits_box(
        items, type("BoxDimensions", (), {
            "dimensions": (box.length, box.width, box.height), "max_weight": box.max_weight
        })()
    )), None)
