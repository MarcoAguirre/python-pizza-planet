from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, jsonify, request

from ..controllers import IngredientController

from .base import BaseService

ingredient = Blueprint('ingredient', __name__)
ingredient_controller = BaseService(IngredientController)


@ingredient.route('/', methods=POST)
def create_ingredient():
    return ingredient_controller.create()


@ingredient.route('/', methods=PUT)
def update_ingredient():
    return ingredient_controller.update()


@ingredient.route('/id/<_id>', methods=GET)
def get_ingredient_by_id(_id: int):
    return ingredient_controller.get_by_id(_id)


@ingredient.route('/', methods=GET)
def get_ingredients():
    return ingredient_controller.get_entity_items()
