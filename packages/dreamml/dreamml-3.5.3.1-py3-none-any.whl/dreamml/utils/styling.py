from typing import Optional
from colorama import Style


class ANSIColoringMixin:
    use_colors: bool

    def _add_ansi_color(self, s: str, color: Optional[str] = None):
        if self.use_colors and color is not None:
            return f"{color}{s}{Style.RESET_ALL}"
        else:
            return s