from .base import ReportBase
from tabulate import tabulate
import argparse


class PositionPerformanceReport(ReportBase):
    """Отчёт по позициям и производительности"""

    def generate(self, data: list[dict], args: argparse.Namespace) -> str:
        table_data = []
        existed_positions: dict[str, list[float]] = {}

        for row in data:
            position = row["position"]
            performance = float(row["performance"])

            if position in existed_positions:
                existed_positions[position].append(performance)
            else:
                existed_positions[position] = [performance]

        for position, performances in existed_positions.items():
            avg_performance = sum(performances) / len(performances)
            table_data.append([position, round(avg_performance, 2)])

        table_data.sort(key=lambda x: x[1], reverse=True)
        return tabulate(table_data, headers=["position", "performance"])

    def get_supported_reports(self) -> list[str]:
        return ["performance"]
