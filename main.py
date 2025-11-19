from helpers import parse_arguments, load_data_from_files
from reports import ReportManager
import sys


def main():
    report_manager = ReportManager()

    args = parse_arguments()

    data = load_data_from_files(args.files)

    report_strategy = report_manager.get_report(args.report)
    if report_strategy:
        if args.result:
            print(f"\nОтчёт: {' '.join(args.result)}\n")

        result = report_strategy.generate(data, args)
        print(f"{result}\n")
    else:
        print(f"Ошибка: Отчёт '{args.report}' не найден.")


main()
