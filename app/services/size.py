from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, jsonify, request

from ..controllers import SizeController

from .base import BaseService

size = Blueprint('size', __name__)
size_controller = BaseService(SizeController)


@size.route('/', methods=POST)
def create_size():
    return size_controller.create()


@size.route('/', methods=PUT)
def update_size():
    return size_controller.update()


@size.route('/id/<_id>', methods=GET)
def get_size_by_id(_id: int):
    return size_controller.get_by_id(_id)


@size.route('/', methods=GET)
def get_sizes():
    return size_controller.get_entity_items()
