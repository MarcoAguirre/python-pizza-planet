import pytest
from app.controllers import ReportController


def test_create_report(app, create_orders):
    created_report = ReportController().create_report()
    pytest.assume(created_report['customer'])
    pytest.assume(created_report['ingredient'])
    pytest.assume(created_report['month'])
