from dataclasses import dataclass

@dataclass
class OrderPayload:
    item_name: str
    quantity: int
    total_cost: int
