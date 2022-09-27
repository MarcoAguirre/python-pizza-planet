from app.common.http_methods import GET, POST
from flask import Blueprint, jsonify, request

from ..controllers import OrderController

from .base import BaseService

order = Blueprint('order', __name__)
order_controller = BaseService(OrderController)


@order.route('/', methods=POST)
def create_order():
    return order_controller.create()


@order.route('/id/<_id>', methods=GET)
def get_order_by_id(_id: int):
    return order_controller.get_by_id(_id)


@order.route('/', methods=GET)
def get_orders():
    return order_controller.get_entity_items()
