import argparse
import csv
from tabulate import tabulate
import sys


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
        "name",
        "position",
        "completed_tasks",
        "performance",
        "skills",
        "team",
        "experience_years",
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


def pos_with_avg(args):
    """
    Отчетность с полями 'postion' и 'performance'.
    Записи из csv группируются по названию позиции и высчитывается среднее арфим. производительности.
    """
    table_data = []
    existed_postions: dict[str, list] = dict()

    for f in args.files:

        with open(f, "r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)
            data_list = list(csv_reader)

            for row in data_list:
                if row["position"] in existed_postions:
                    existed_postions[row["position"]].append(row[args.report])
                else:
                    existed_postions[row["position"]] = [row[args.report]]

    for positions in existed_postions:
        avg = 0.0
        for performance in existed_postions[positions]:
            avg += float(performance)
        table_data.append([positions, round(avg / len(existed_postions[positions]), 2)])

    table_data.sort(key=lambda x: x[1], reverse=True)
    return tabulate(table_data, headers=["postition", args.report])


if __name__ == "__main__":
    args = parse_arguments()
    if args.report == "performance":
        if args.result:
            print(f"\n\nОтчёт: {(" ").join(args.result)}\n\n")
        print(pos_with_avg(args))
    else:
        print(f"Отчётность для {args.report} ещё не разработана.")
