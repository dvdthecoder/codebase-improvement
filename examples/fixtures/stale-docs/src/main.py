"""Fixture implementation: negative values are rejected."""

def calculate_total(quantity: int, unit_price: int) -> int:
    if quantity < 0:
        raise ValueError("quantity must not be negative")
    if unit_price < 0:
        raise ValueError("unit_price must not be negative")
    return quantity * unit_price
