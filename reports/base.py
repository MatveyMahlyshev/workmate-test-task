from abc import ABC, abstractmethod
import argparse


class ReportBase(ABC):

    @abstractmethod
    def generate(
        self,
        data: list[dict],
        args: argparse.Namespace,
    ) -> str:
        pass

    @abstractmethod
    def get_supported_reports(self) -> list[str]:
        pass
