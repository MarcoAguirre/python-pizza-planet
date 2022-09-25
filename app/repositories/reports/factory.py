from abc import ABC, abstractmethod

from app.repositories.models import Ingredient, Order, IngredientDetail, db
from .report_manager import IReport, ReportManager


class IReportFactory(ABC):
    @abstractmethod
    def get_created_report(self) -> IReport:
        pass


class ReportFactory(IReportFactory):
    def __init__(self):
        self._session = db.session
        self._order = Order
        self._ingredient_detail = IngredientDetail
        self._ingredient = Ingredient

    def get_created_report(self) -> IReport:
        return ReportManager(self._session, self._order, self._ingredient_detail, self._ingredient)
