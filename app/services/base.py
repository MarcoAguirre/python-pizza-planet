from app.common.http_methods import GET, POST, PUT
from flask import jsonify, request

from ..controllers.base import BaseController


class BaseService():

    def __init__(self, base_controller: BaseController):
        self.base_controller = base_controller

    def create(self):
        base_controller, error = self.base_controller.create(request.json)
        response = base_controller if not error else {'error': error}
        status_code = 200 if not error else 400
        return jsonify(response), status_code

    def update(self):
        base_controller, error = self.base_controller.update(request.json)
        response = base_controller if not error else {'error': error}
        status_code = 200 if not error else 400
        return jsonify(response), status_code

    def get_by_id(self, _id: int):
        base_controller, error = self.base_controller.get_by_id(_id)
        response = base_controller if not error else {'error': error}
        status_code = 200 if base_controller else 404 if not error else 400
        return jsonify(response), status_code

    def get_entity_items(self):
        entities, error = self.base_controller.get_all()
        response = entities if not error else {'error': error}
        status_code = 200 if entities else 404 if not error else 400
        return jsonify(response), status_code
