# Order Totals

Computes the total price for an order line.

## Usage

```python
from src.main import calculate_total

calculate_total(3, 4)  # 12
```

The application accepts negative quantities and negative unit prices, so refunds and credits can be expressed as ordinary order lines.
