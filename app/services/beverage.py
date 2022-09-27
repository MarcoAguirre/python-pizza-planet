from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, jsonify, request

from ..controllers import BeverageController

from .base import BaseService

beverage = Blueprint('beverage', __name__)
beverage_controller = BaseService(BeverageController)


@beverage.route('/', methods=POST)
def create_beverage():
    return beverage_controller.create()


@beverage.route('/', methods=PUT)
def update_beverage():
    return beverage_controller.update()


@beverage.route('/id/<_id>', methods=GET)
def get_beverage_by_id(_id: int):
    return beverage_controller.get_by_id(_id)


@beverage.route('/', methods=GET)
def get_beverages():
    return beverage_controller.get_entity_items()
