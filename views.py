from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from builder import build_query
from models import RequestSchema, BatchRequestSchema

main_bp = Blueprint('main', __name__)

# FILE_NAME = 'data/apache_logs.txt'


@main_bp.route("/perform_query", methods=['POST'])
def perform_query():
    # получить параметры query и file_name из request.args, при ошибке вернуть ошибку 400
    # проверить, что файла file_name существует в папке DATA_DIR, при ошибке вернуть ошибку 400
    # с помощью функционального программирования (функций filter, map), итераторов/генераторов сконструировать запрос
    # вернуть пользователю сформированный результат
    # return app.response_class('', content_type="text/plain")
    data = request.json

    try:
        validate_data = BatchRequestSchema().load(data)
    except ValidationError as error:
        return jsonify(error.messages), 400

    result = None
    for query in validate_data['queries']:
        result = build_query(
            cmd=query['cmd'],
            value=query['value'],
            # file_name=query['file_name'],
            file_name=validate_data['file_name'],
            data=result,
        )

    return jsonify(result)
