import pandas as pd
from flask import Blueprint, jsonify, request, send_file

from .controllers import (
    create_record,
    export_to_excel,
    get_all_records,
    process_dataframe_for_bulk_create,
    process_dataframe_for_bulk_update,
    update_record,
)

bp = Blueprint("api", __name__)


@bp.route("/create", methods=["POST"])
def create():
    data = request.get_json()
    return jsonify(create_record(data))


@bp.route("/bulk_create", methods=["POST"])
def upload_bulk_create():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    if not file.filename.endswith(".xlsx"):
        return jsonify({"error": "File format not supported, please upload an .xlsx file"}), 400

    # Load Excel into DataFrame
    try:
        df = pd.read_excel(file)
        response = process_dataframe_for_bulk_create(df)
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": f"Failed to process the file: {str(e)}"}), 500


@bp.route("/records", methods=["GET"])
def get_all():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    records = get_all_records(page, per_page)
    return jsonify(records)


@bp.route("/update/<int:record_id>", methods=["PUT"])
def update(record_id):
    data = request.get_json()
    return jsonify(update_record(record_id, data))


@bp.route("/bulk_update", methods=["PUT"])
def upload_bulk_update():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    if not file.filename.endswith(".xlsx"):
        return jsonify({"error": "File format not supported, please upload an .xlsx file"}), 400

    # Load Excel into DataFrame
    try:
        df = pd.read_excel(file)
        response = process_dataframe_for_bulk_update(df)
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": f"Failed to process the file: {str(e)}"}), 500


@bp.route("/export", methods=["GET"])
def export():
    file_path = export_to_excel()
    return send_file(file_path, as_attachment=True, download_name="exported_data.xlsx")
