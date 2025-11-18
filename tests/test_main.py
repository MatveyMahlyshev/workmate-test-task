import sys
from unittest.mock import patch, MagicMock
import pytest

from main import parse_arguments, pos_with_avg


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


class TestPosWithAvg:
    """Тесты для функции pos_with_avg"""

    @pytest.fixture
    def sample_csv_data(self):
        """Фикстура с тестовыми CSV данными"""
        return """name,position,completed_tasks,performance,skills,team,experience_years
Alex Ivanov,Backend Developer,45,4.8,Python,API Team,5
Maria Petrova,Frontend Developer,38,4.7,React,Web Team,4
John Smith,Backend Developer,29,4.6,Python,AI Team,3
Anna Lee,Frontend Developer,52,4.9,JavaScript,Infrastructure Team,6"""

    @pytest.fixture
    def mock_args(self):
        """Фикстура с mock аргументами"""
        args = MagicMock()
        args.files = ["test.csv"]
        args.report = "performance"
        return args

    def test_pos_with_avg_calculation(self, sample_csv_data, mock_args, tmp_path):
        """Тест расчета средних значений"""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(sample_csv_data, encoding="utf-8")
        mock_args.files = [str(csv_file)]

        result = pos_with_avg(mock_args)

        assert "Backend Developer" in result
        assert "Frontend Developer" in result
        assert "4.7" in result
        assert "4.8" in result

    def test_pos_with_avg_sorting(self, sample_csv_data, mock_args, tmp_path):
        """Тест сортировки результатов"""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(sample_csv_data, encoding="utf-8")
        mock_args.files = [str(csv_file)]

        result = pos_with_avg(mock_args)

        lines = result.split("\n")
        data_lines = [line for line in lines if "Developer" in line]

        assert "Frontend Developer" in data_lines[0]
        assert "Backend Developer" in data_lines[1]

    def test_pos_with_avg_multiple_files(self, sample_csv_data, mock_args, tmp_path):
        """Тест с несколькими файлами"""
        csv_file1 = tmp_path / "test1.csv"
        csv_file2 = tmp_path / "test2.csv"

        csv_file1.write_text(sample_csv_data, encoding="utf-8")
        csv_file2.write_text(sample_csv_data, encoding="utf-8")

        mock_args.files = [str(csv_file1), str(csv_file2)]

        result = pos_with_avg(mock_args)

        assert "Backend Developer" in result
        assert "Frontend Developer" in result

    def test_file_not_found(self, mock_args):
        """Тест с несуществующим файлом"""
        mock_args.files = ["nonexistent.csv"]

        with pytest.raises(FileNotFoundError):
            pos_with_avg(mock_args)
