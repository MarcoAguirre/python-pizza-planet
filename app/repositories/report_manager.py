from typing import Optional, Sequence

from .models import Ingredient, Order, IngredientDetail, db

from sqlalchemy import func, desc


class BaseReportManager:
    order_model: Optional[db.Model] = None
    ingredient_detail_model: Optional[db.Model] = None
    session = db.session

    @classmethod
    def get_most_requested_ingredients(cls):
        ingredients_chosen_count = cls.session.query(func.count(cls.ingredient_detail_model.ingredient_id).label('count'),
                                                     cls.ingredient_detail_model.ingredient_id).group_by(
            cls.ingredient_detail_model.ingredient_id).order_by(desc('count')).first()

        ingredient = Ingredient.query.get(
            ingredients_chosen_count.ingredient_id)

        most_requested_ingredient = {
            'name': ingredient.name,
            'count': ingredients_chosen_count.count
        }

        return most_requested_ingredient

    @classmethod
    def get_month_with_more_revenue(cls):
        more_revenued_months = cls.session.query(func.strftime("%m", cls.order_model.date).label('month'),
                                                 func.sum(cls.order_model.total_price).label('total')).group_by(
            'month').order_by(desc('total')).first()

        return {'month_number': more_revenued_months[0], 'total': more_revenued_months[1]}

    @classmethod
    def get_more_loyal_customer(cls):
        loyal_customer = cls.session.query(cls.order_model.client_name, cls.order_model.client_dni,
                                           func.count(cls.order_model.client_dni).label(
                                               'count')
                                           ).group_by(cls.order_model.client_dni).order_by(desc('count')).limit(3).all()

        return [{'position': pos + 1, 'name': customer.client_name, 'dni': customer.client_dni}
                for pos, customer in enumerate(loyal_customer)]


class ReportManager(BaseReportManager):
    order_model = Order
    ingredient_detail_model = IngredientDetail

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
