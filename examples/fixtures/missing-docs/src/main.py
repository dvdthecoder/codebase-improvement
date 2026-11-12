"""Small fixture: source exists, but no repository documentation is provided."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    item_id: str
    quantity: int


def calculate_total(items: list[Item], unit_price: int) -> int:
    """Return the total in minor currency units."""
    if unit_price < 0:
        raise ValueError("unit_price must not be negative")
    if any(item.quantity < 0 for item in items):
        raise ValueError("quantity must not be negative")
    return sum(item.quantity for item in items) * unit_price


def main() -> None:
    print(calculate_total([Item("A-1", 2)], 125))


if __name__ == "__main__":
    main()
