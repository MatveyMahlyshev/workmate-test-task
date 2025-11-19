import argparse
import sys
import csv


def parse_arguments():
    """Парс аргументов из терминала."""
    parser = argparse.ArgumentParser(
        description="Генератор отчётов по сотрудникам.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "--files",
        type=str,
        required=True,
        nargs="+",
        help="Путь к CSV-файлу.",
    )

    report_choices = [
        "performance",
    ]

    parser.add_argument(
        "--report",
        type=str,
        required=True,
        choices=report_choices,
    )

    parser.add_argument(
        "--result",
        type=str,
        required=False,
        nargs="+",
    )

    try:
        return parser.parse_args()
    except SystemExit:
        print("\nВы неправильно ввели аргументы при запуске скрипта.\n")
        print("Доступные типы отчетов:")
        for choice in report_choices:
            print(choice)
        print(
            f"\nПример: \npython3 {sys.argv[0]} --files employees.csv --report performance \nили "
        )
        print(
            "python3 main.py --files  files/employees1.csv files/employees2.csv --report performance --result Позиция и Производительность"
        )
        sys.exit(1)


def load_data_from_files(files: list[str]) -> list[dict]:
    """Загрузка данных из CSV файлов"""
    all_data = []
    for file_path in files:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                csv_reader = csv.DictReader(file)
                all_data.extend(list(csv_reader))
        except FileNotFoundError:
            print(f"Ошибка: файл {file_path} не найден")
            sys.exit(1)
        except Exception as e:
            print(f"Ошибка при чтении файла {file_path}: {e}")
            sys.exit(1)
    return all_data
