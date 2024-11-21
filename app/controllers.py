import pandas as pd
from flask import abort
from flask import send_file
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text

from io import BytesIO

from . import db
from .models import Assets


def create_record(data):
    try:
        record = Assets(**data)
        db.session.add(record)
        db.session.commit()
        return record.to_dict(), 201  # todo rewrite
    except Exception as e:
        db.session.rollback()
        abort(400, description=str(e))


def bulk_create_records(data):
    assets = [Assets(**item) for item in data]
    db.session.bulk_save_objects(assets)
    db.session.commit()
    return {"message": f"{len(assets)} records created successfully"}, 201


def process_dataframe_for_bulk_create(df):
    assets = [
        Assets(
            name=row["name"],
            barcode=row["barcode"],
            barcode_type=row["barcode_type"],
            individual_asset_reference=row["individual_asset_reference"],
            asset_type=row["asset_type"],
            asset_description=row.get("asset_description"),
            manufacturer_name=row.get("manufacturer_name"),
            gln=row["gln"],
            current_status=row.get("current_status"),
            asset_condition=row.get("asset_condition"),
            contact_point_name=row.get("contact_point_name"),
            contact_point_email=row.get("contact_point_email"),
            contact_point_telephone=row.get("contact_point_telephone"),
        )
        for _, row in df.iterrows()
    ]
    print(assets[0].name)  # Optional: just for debugging
    db.session.bulk_save_objects(assets)
    db.session.commit()
    return {"message": f"{len(assets)} records created successfully"}, 201


def get_all_records(page, per_page):
    records = Assets.query.paginate(page=page, per_page=per_page)
    return [record.to_dict() for record in records.items]


def get_total_records_count():
    query = "SELECT COUNT(*) FROM assets"
    result = db.session.execute(text(query)).scalar()
    return result


def update_record(record_id, data):
    record = Assets.query.get(record_id)
    if record is None:
        abort(404)
    for key, value in data.items():
        setattr(record, key, value)
    db.session.commit()
    return record.to_dict()


def process_dataframe_for_bulk_update(df):
    updated_count = 0
    not_found_barcodes = []
    df["barcode"] = df["barcode"].astype(str)

    for _, row in df.iterrows():
        # Fetch the existing asset based on the barcode
        asset = Assets.query.filter_by(barcode=str(row["barcode"])).first()

        if asset:
            # Update fields with new values from the DataFrame
            asset.name = row.get("name", asset.name)
            asset.barcode_type = row.get("barcode_type", asset.barcode_type)
            asset.individual_asset_reference = row.get(
                "individual_asset_reference", asset.individual_asset_reference
            )
            asset.asset_type = row.get("asset_type", asset.asset_type)
            asset.asset_description = row.get(
                "asset_description", asset.asset_description
            )
            asset.manufacturer_name = row.get(
                "manufacturer_name", asset.manufacturer_name
            )
            asset.gln = row.get("gln", asset.gln)
            asset.current_status = row.get("current_status", asset.current_status)
            asset.asset_condition = row.get("asset_condition", asset.asset_condition)
            asset.contact_point_name = row.get(
                "contact_point_name", asset.contact_point_name
            )
            asset.contact_point_email = row.get(
                "contact_point_email", asset.contact_point_email
            )
            asset.contact_point_telephone = row.get(
                "contact_point_telephone", asset.contact_point_telephone
            )

            updated_count += 1
        else:
            # If barcode is not found, add it to a list for tracking
            not_found_barcodes.append(row["barcode"])

    # Attempt to commit the changes to the database
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": f"Failed to update records: {str(e)}"}, 500

    # Response message with details
    response = {
        "message": f"{updated_count} records updated successfully",
        "not_found_barcodes": not_found_barcodes,
    }
    return response, 200


def export_to_excel():
    records = Assets.query.all()
    df = pd.DataFrame([record.to_dict() for record in records])

    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    output.seek(0)

    # Return as an in-memory file to avoid saving on disk
    return send_file(
        output,
        as_attachment=True,
        download_name="exported_data.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    ### The below is intended to test the route with POSTMAN and results in an excel file
    # records = Assets.query.all()
    # df = pd.DataFrame([record.to_dict() for record in records])
    # file_path = "/tmp/exported_data.xlsx"
    # df.to_excel(file_path, index=False)
    # return file_path
