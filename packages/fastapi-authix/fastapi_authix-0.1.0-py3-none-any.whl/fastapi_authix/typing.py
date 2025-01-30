from typing import Literal

SerializeMode = Literal[
    "auto",
    "dict",
    "dataclass",
    "pydantic",
    "sqlalchemy",
]
