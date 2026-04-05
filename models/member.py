from dataclasses import dataclass
from typing import Optional

@dataclass
class Member:
    name:          str
    email:         str
    membership_id: str
    id:            Optional[int] = None