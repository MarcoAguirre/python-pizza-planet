from ..repositories.report_manager import ReportManager
from ..repositories.report_manager import BaseReportManager


class ReportController(BaseReportManager):
    manager = ReportManager

    def create_report(self):
        return self.manager.create_report()
