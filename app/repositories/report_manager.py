from typing import Any, List, Optional, Sequence

from .models import BeverageDetail, Ingredient, Order, IngredientDetail, Size, Beverage, db

from sqlalchemy import func, desc


class BaseReportManager:
    order_model: Optional[db.Model] = None
    ingredient_detail_model: Optional[db.Model] = None
    session = db.session

    @classmethod
    def get_most_requested_ingredients(cls):
        ingredients_chosen_count = cls.session.query(func.count(cls.order_detail_model.ingredient_id).label('count'),
                                                     cls.order_detail_model.ingredient_id).group_by(
            cls.order_detail_model.ingredient_id).order_by(desc('count')).first()

        ingredient = Ingredient.query.get(
            ingredients_chosen_count.ingredient_id)

        most_requested_ingredient = {
            'name': ingredient.name,
            'count': ingredients_chosen_count.count
        }

        return most_requested_ingredient

    @ classmethod
    def get_month_with_more_revenue(cls):
        more_revenued_months = cls.session.query(func.strftime("%m", cls.order_model.date).label('month'),
                                                 func.sum(cls.order_model.total_price).label('total')).group_by(
            'month').order_by(desc('total')).first()

        return {'month_number': more_revenued_months[0], 'total': more_revenued_months[1]}

    @ classmethod
    def get_more_loyal_customer(cls):
        loyal_customer = cls.session.query()


class ReportManager:
    pass
