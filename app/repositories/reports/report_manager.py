from abc import ABC, abstractmethod
from typing import Optional, Sequence

from ..models import Ingredient, Order, IngredientDetail, db

from sqlalchemy import func, desc


class IReport(ABC):

    @abstractmethod
    def create_report() -> dict:
        pass


class ReportManager(IReport):
    def __init__(cls, session: db.session, order: db.Model, ingredient_detail: db.Model, ingredient: db.Model):
        cls._session = session
        cls._order = order
        cls._ingredient_detail = ingredient_detail
        cls._ingredient = ingredient

    @classmethod
    def get_most_requested_ingredients(cls):
        ingredients_chosen_count = cls._session.query(func.count(cls._ingredient_detail.ingredient_id).label('count'),
                                                      cls._ingredient_detail.ingredient_id).group_by(
            cls._ingredient_detail.ingredient_id).order_by(desc('count')).first()

        ingredient = cls._ingredient.query.get(
            ingredients_chosen_count.ingredient_id)

        most_requested_ingredient = {
            'name': ingredient.name,
            'count': ingredients_chosen_count.count
        }

        return most_requested_ingredient

    @classmethod
    def get_month_with_more_revenue(cls):
        more_revenued_months = cls._session.query(func.strftime("%m", cls._order.date).label('month'),
                                                  func.sum(cls._order.total_price).label('total')).group_by(
            'month').order_by(desc('total')).first()

        return {'month_number': more_revenued_months[0], 'total': more_revenued_months[1]}

    @classmethod
    def get_more_loyal_customer(cls):
        loyal_customer = cls._session.query(cls._order.client_name, cls._order.client_dni,
                                            func.count(cls._order.client_dni).label(
                                                'count')
                                            ).group_by(cls._order.client_dni).order_by(desc('count')).limit(3).all()

        return [{'position': pos + 1, 'name': customer.client_name, 'dni': customer.client_dni}
                for pos, customer in enumerate(loyal_customer)]

    @classmethod
    def create_report(cls):
        most_requested_ingredient = cls.get_most_requested_ingredients()
        most_revenued_months = cls.get_month_with_more_revenue()
        most_loyal_customer = cls.get_more_loyal_customer()

        return {
            'ingredient': most_requested_ingredient,
            'month': most_revenued_months,
            'customer': most_loyal_customer
        }
