from . import ReportBase, PositionPerformanceReport


class ReportManager:

    def __init__(self):
        self.reports: dict[ReportBase] = {}
        self.register_default_reports()

    def register_default_reports(self):
        self.register_report(PositionPerformanceReport())

    def register_report(
        self,
        report: ReportBase,
    ):
        for report_type in report.get_supported_reports():
            self.reports[report_type] = report

    def get_report(
        self,
        report_type: str,
    ) -> ReportBase:
        return self.reports.get(report_type)
