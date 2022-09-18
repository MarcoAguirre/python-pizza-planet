import pytest
from app.controllers import ReportController


def test_create_report(app):
    created_report, error = ReportController().create_report()
    pytest.assume(error is None)
    pytest.assume(created_report['customer'])
    pytest.assume(created_report['ingredient'])
    pytest.assume(created_report['beverage'])
    pytest.assume(created_report['size'])
    pytest.assume(created_report['month'])
