from ..repositories.report_manager import ReportManager
from .base import BaseController


class ReportController(BaseController):
    manager = ReportManager
