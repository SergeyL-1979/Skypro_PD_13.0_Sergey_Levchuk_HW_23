from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from builder import build_query
from models import RequestSchema, BatchRequestSchema

main_bp = Blueprint('main', __name__)

# FILE_NAME = 'data/apache_logs.txt'


@main_bp.route("/perform_query", methods=['POST'])
def perform_query():
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
