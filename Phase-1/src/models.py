from dataclasses import dataclass

@dataclass
class Task:
    """Represents a to-do item."""
    id: int
    description: str
    completed: bool = False
