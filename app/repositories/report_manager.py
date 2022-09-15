from typing import Any, List, Optional, Sequence

from .models import BeverageDetail, Ingredient, Order, IngredientDetail, Size, Beverage, db

from sqlalchemy import func


class BaseReportManager:
    order_model: Optional[db.Model] = None
    ingredient_detail_model: Optional[db.Model] = None
    session = db.session

    @classmethod
    def get_most_requested_ingredients(cls):
        ingredients_gotten = cls.session.query()

    @classmethod
    def get_month_with_more_revenue(cls):
        months_gotten = cls.session.query()

    @classmethod
    def get_more_loyal_customer(cls):
        loyal_customer = cls.session.query()
