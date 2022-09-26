from..repositories.reports.factory import ReportFactory


class ReportController():
    def create_report(self):
        return ReportFactory().get_created_report().create_report()
