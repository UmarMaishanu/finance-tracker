from dataclasses import dataclass
from typing import Optional

@dataclass
class Budget:
    category: str
    limit:    float
    id:       Optional[int] = None