from pathlib import Path
from typing import Protocol

import pandas as pd

from .models import AutomationResult


class ReportGenerator(Protocol):
    """
    Defines the interface for a report generator.
    """

    def build(self, result: AutomationResult) -> str:
        ...

    def write(self, report_text: str, output_dir: str = "reports") -> Path:
        ...
