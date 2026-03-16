from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Rect:
    x_1: float
    y_1: float
    x_2: float | None = None
    y_2: float | None = None

    def point(self) -> tuple[float, float]:
        return (self.x_1, self.y_1)

    def width(self) -> float:
        if self.x_2 is None:
            return 0.0
        return self.x_2 - self.x_1

    def height(self) -> float:
        if self.y_2 is None:
            return 0.0
        return self.y_2 - self.y_1

    def contains(self, x: float, y: float) -> bool:
        if self.x_2 is None or self.y_2 is None:
            return False
        return self.x_1 < x < self.x_2 and self.y_1 < y < self.y_2


@dataclass(frozen=True)
class DragState:
    name: str | None = None
    offset_x: float | None = None
    offset_y: float | None = None

    @property
    def active(self) -> bool:
        return self.name is not None
