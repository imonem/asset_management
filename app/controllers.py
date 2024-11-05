from flask import jsonify, request, abort
from . import db
from .models import Assets
import pandas as pd

def create_record(data):
    try:
        record = Assets(**data)
        db.session.add(record)
        db.session.commit()
        # return record.to_dict(), 201 # todo rewrite
    except Exception as e:
        db.session.rollback()
        abort(400, description=str(e))

def get_all_records(page, per_page):
    records = Assets.query.paginate(page=page, per_page=per_page)
    return [record.to_dict() for record in records.items]

def update_record(record_id, data):
    record = Assets.query.get(record_id)
    if record is None:
        abort(404)
    for key, value in data.items():
        setattr(record, key, value)
    db.session.commit()
    return record.to_dict()

def export_to_excel():
    records = Assets.query.all()
    df = pd.DataFrame([record.to_dict() for record in records])
    file_path = '/tmp/exported_data.xlsx'
    df.to_excel(file_path, index=False)
    return file_path
