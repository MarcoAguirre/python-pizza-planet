from abc import ABC, abstractmethod

from sqlalchemy import func, desc

from ..models import db


class IReport(ABC):

    @abstractmethod
    def create_report() -> dict:
        pass


class ReportManager(IReport):
    def __init__(self, session: db.session, order: db.Model, ingredient_detail: db.Model, ingredient: db.Model):
        self._session = session
        self._order = order
        self._ingredient_detail = ingredient_detail
        self._ingredient = ingredient

    def get_most_requested_ingredients(self):
        ingredients_chosen_count = self._session.query(func.count(self._ingredient_detail.ingredient_id).label('count'),
                                                       self._ingredient_detail.ingredient_id).group_by(
            self._ingredient_detail.ingredient_id).order_by(desc('count')).first()

        ingredient = self._ingredient.query.get(
            ingredients_chosen_count.ingredient_id)

        most_requested_ingredient = {
            'name': ingredient.name,
            'count': ingredients_chosen_count.count
        }

        return most_requested_ingredient

    def get_month_with_more_revenue(self):
        more_revenued_months = self._session.query(func.strftime("%m", self._order.date).label('month'),
                                                   func.sum(self._order.total_price).label('total')).group_by(
            'month').order_by(desc('total')).first()

        return {'month_number': more_revenued_months[0], 'total': more_revenued_months[1]}

    def get_more_loyal_customer(self):
        loyal_customer = self._session.query(self._order.client_name, self._order.client_dni,
                                             func.count(self._order.client_dni).label(
                                                 'count')
                                             ).group_by(self._order.client_dni).order_by(desc('count')).limit(3).all()

        return [{'position': pos + 1, 'name': customer.client_name, 'dni': customer.client_dni}
                for pos, customer in enumerate(loyal_customer)]

    def create_report(self):
        most_requested_ingredient = self.get_most_requested_ingredients()
        most_revenued_months = self.get_month_with_more_revenue()
        most_loyal_customer = self.get_more_loyal_customer()

        return {
            'ingredient': most_requested_ingredient,
            'month': most_revenued_months,
            'customer': most_loyal_customer
        }
