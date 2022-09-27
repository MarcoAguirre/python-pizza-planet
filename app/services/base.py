from app.common.http_methods import GET, POST, PUT
from flask import jsonify, request

from ..controllers import base


class BaseService():

    def __init__(cls, entity: base):
        cls.entity = entity

    def create(cls, request):
        entity, error = cls.entity.create(request.json)
        response = entity if not error else {'error': error}
        status_code = 200 if not error else 400
        return jsonify(response), status_code

    def update(cls):
        entity, error = cls.entity.update(request.json)
        response = entity if not error else {'error': error}
        status_code = 200 if not error else 400
        return jsonify(response), status_code

    def get_by_id(cls, _id: int):
        entity, error = cls.entity.get_by_id(_id)
        response = entity if not error else {'error': error}
        status_code = 200 if entity else 404 if not error else 400
        return jsonify(response), status_code

    def get_entity_items(cls):
        entities, error = cls.entity.get_all()
        response = entities if not error else {'error': error}
        status_code = 200 if entities else 404 if not error else 400
        return jsonify(response), status_code
