from . import db

class YourModel(db.Model):
    __tablename__ = 'your_table'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    barcode = db.column(db.string(30), nullable=False)
    barcode_type = db.column(db.string(4), nullable=False)
    individual_asset_reference = db.column(db.string(), nullable=False)
    asset_type = db.column(db.string(), nullable=False)
    asset_description = db.column(db.string(), nullable=True)
    manufacturer_name = db.column(db.string(), nullable=True)
    gln = db.column(db.string(), nullable=False)
    current_status = db.column(db.string(), nullable=True)
    asset_condition = db.column(db.string(), nullable=True)
    contact_point_name = db.column(db.string(), nullable=True)
    contact_point_email = db.column(db.string(), nullable=True)
    contact_point_telephone = db.Column(db.String(), nullable=True)

    # Define other fields here

    def to_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}