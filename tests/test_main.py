import sys
from unittest.mock import patch, MagicMock
import pytest
import argparse

from reports import ReportManager, ReportBase, PositionPerformanceReport
from helpers import parse_arguments


class TestParseArguments:
    """Тесты для функции parse_arguments"""

    def test_valid_arguments(self):
        """Тест с правильными аргументами"""
        test_args = ["--files", "test.csv", "--report", "performance"]

        with patch.object(sys, "argv", ["main.py"] + test_args):
            args = parse_arguments()

            assert args.files == ["test.csv"]
            assert args.report == "performance"

    def test_valid_arguments_with_result(self):
        """Тест с правильными аргументами и названием отчёта"""
        test_args = [
            "--files",
            "test.csv",
            "--report",
            "performance",
            "--result",
            "Позиция и Производительность",
        ]

        with patch.object(sys, "argv", ["main.py"] + test_args):
            args = parse_arguments()

            assert args.files == ["test.csv"]
            assert args.report == "performance"
            assert args.result[0] == "Позиция и Производительность"

    def test_valid_arguments_with_empty_result(self, capsys):
        """Тест с пустым результатом"""
        test_args = ["--files", "test.csv", "--report", "performance", "--result"]

        with patch.object(sys, "argv", ["main.py"] + test_args):
            with pytest.raises(SystemExit):
                parse_arguments()

            captured = capsys.readouterr()

            assert "Вы неправильно ввели аргументы" in captured.out

    def test_multiple_files(self):
        """Тест с правильными аргументами и несколькими файлами"""
        test_args = ["--files", "test.csv", "test2.csv", "--report", "performance"]

        with patch.object(sys, "argv", ["main.py"] + test_args):
            args = parse_arguments()

            assert args.files == ["test.csv", "test2.csv"]
            assert args.report == "performance"

    def test_invalid_report_type(self, capsys):
        """Тест с неправильным типом отчета"""
        test_args = ["--files", "test.csv", "--report", "invalid_report"]

        with patch.object(sys, "argv", ["main.py"] + test_args):
            with pytest.raises(SystemExit):
                parse_arguments()

            captured = capsys.readouterr()
            assert "Вы неправильно ввели аргументы" in captured.out
            assert "performance" in captured.out

    def test_missing_required_args(self, capsys):
        """Не хватает --report"""
        test_args = ["--files", "test.csv"]

        with patch.object(sys, "argv", ["main.py"] + test_args):
            with pytest.raises(SystemExit):
                parse_arguments()

            captured = capsys.readouterr()
            assert "Вы неправильно ввели аргументы" in captured.out


class TestReportBase:
    """Тесты для базового класса отчётов"""

    def test_report_base_is_abstract(self):
        with pytest.raises(TypeError):
            ReportBase()


class TestPositionPerformanceReport:
    """Тесты для отчёта по производительности"""

    @pytest.fixture
    def report(self):
        return PositionPerformanceReport()

    @pytest.fixture
    def sample_data(self):
        return [
            {"name": "Иван", "position": "Developer", "performance": "0.8"},
            {"name": "Петр", "position": "Developer", "performance": "0.9"},
            {"name": "Мария", "position": "Designer", "performance": "0.7"},
            {"name": "Анна", "position": "Designer", "performance": "0.85"},
        ]

    @pytest.fixture
    def mock_args(self):
        args = MagicMock(spec=argparse.Namespace)
        args.report = "performance"
        args.result = None
        return args

    def test_get_supported_reports(self, report):
        """Тест поддерживаемых отчётов"""
        supported = report.get_supported_reports()
        assert supported == ["performance"]
        assert isinstance(supported, list)

    def test_generate_report(self, report, sample_data, mock_args):
        """Тест генерации отчёта"""
        result = report.generate(sample_data, mock_args)

        assert "Developer" in result
        assert "Designer" in result
        assert "0.85" in result 
        assert "0.77" in result  

    def test_generate_report_sorting(self, report, sample_data, mock_args):
        """Тест сортировки результатов по убыванию"""
        result = report.generate(sample_data, mock_args)
        lines = result.split("\n")

        data_lines = [
            line for line in lines if "Developer" in line or "Designer" in line
        ]
        assert (
            "Developer" in data_lines[0]
        )  
        assert "Designer" in data_lines[1]

    def test_generate_empty_data(self, report, mock_args):
        """Тест с пустыми данными"""
        result = report.generate([], mock_args)
        assert "position" in result  
        assert "performance" in result


class TestReportManager:
    """Тесты для менеджера отчётов"""

    @pytest.fixture
    def manager(self):
        return ReportManager()

    def test_initialization(self, manager):
        """Тест инициализации менеджера"""
        assert hasattr(manager, "reports")
        assert isinstance(manager.reports, dict)

    def test_get_report_existing(self, manager):
        """Тест получения существующего отчёта"""
        report = manager.get_report("performance")
        assert report is not None
        assert isinstance(report, PositionPerformanceReport)

    def test_get_report_nonexistent(self, manager):
        """Тест получения несуществующего отчёта"""
        report = manager.get_report("nonexistent")
        assert report is None

    def test_register_new_report(self, manager):
        """Тест регистрации нового отчёта"""

        class TestReport(ReportBase):
            def generate(self, data, args):
                return "test report"

            def get_supported_reports(self):
                return ["test_report"]

        test_report = TestReport()
        manager.register_report(test_report)

        assert manager.get_report("test_report") == test_report

    def test_register_report_multiple_types(self, manager):
        """Тест регистрации отчёта с несколькими типами"""

        class MultiReport(ReportBase):
            def generate(self, data, args):
                return "multi report"

            def get_supported_reports(self):
                return ["type1", "type2", "type3"]

        multi_report = MultiReport()
        manager.register_report(multi_report)

        assert manager.get_report("type1") == multi_report
        assert manager.get_report("type2") == multi_report
