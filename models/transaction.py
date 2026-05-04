from dataclasses import dataclass
from typing import Optional

@dataclass
class Transaction:
    description:      str
    amount:           float
    category:         str
    transaction_type: str
    date:             str
    status:           str = "pending"
    id:               Optional[int] = None