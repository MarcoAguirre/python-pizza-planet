from ..repositories.report_manager import ReportManager
from ..repositories.report_manager import BaseReportManager


class ReportController(BaseReportManager):
    manager = ReportManager
