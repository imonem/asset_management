from flask import Blueprint, request, jsonify, send_file
from .controllers import create_record, get_all_records, update_record, export_to_excel

bp = Blueprint('api', __name__)

@bp.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    return jsonify(create_record(data))

@bp.route('/records', methods=['GET'])
def get_all():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    records = get_all_records(page, per_page)
    return jsonify(records)

@bp.route('/update/<int:record_id>', methods=['PUT'])
def update(record_id):
    data = request.get_json()
    return jsonify(update_record(record_id, data))

@bp.route('/export', methods=['GET'])
def export():
    file_path = export_to_excel()
    return send_file(file_path, as_attachment=True, download_name='exported_data.xlsx')
