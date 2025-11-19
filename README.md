# workmate-test-task
Тестовое задание на роль Junior Python Developer.

# Установка зависимостей
- клонировать репозиторий
- установить виртуальное окружение(например, python3 -m venv venv)
- активировать виртуальное окружение(например, source venv/bin/activate)
- установить зависимости(pip install -r requirements.txt)

# Запуск скрипта
- Без названия отчёта: python3 main.py --files files/employees1.csv files/employees2.csv --report performance
- С названием отчёта: python3 main.py --files files/employees1.csv files/employees2.csv --report performance --result Тестовый отчёт



- В папке проекта лежат отчёты в виде изображений.

- В папке files лежат два csv-файла с данными.


# Добавление нового отчёта

Чтобы добавить новый отчёт нужно:
- в пакете "reports" создать python-модуль
- в этом модуле создать класс, унаследовать его от абстрактного класса ReportBase.
- реализовать методы generate(генерирует отчёт) и get_supported_reports(возвращает поддерживаемые отчёты)
- в классе ReportManager в методе register_default_reports нужно зарегистрировать отчёт с помощью метода register_report
