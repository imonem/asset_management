from . import db


class Assets(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    name = db.Column(db.String(100), nullable=False)
    barcode = db.Column(db.String(30), nullable=False)
    barcode_type = db.Column(db.String(4), nullable=False)
    individual_asset_reference = db.Column(db.String(30), nullable=False)
    asset_type = db.Column(db.String(30), nullable=False)
    asset_description = db.Column(db.String(256), nullable=True)
    manufacturer_name = db.Column(db.String(50), nullable=True)
    gln = db.Column(db.String(14), nullable=False)
    current_status = db.Column(db.String(20), nullable=True)
    asset_condition = db.Column(db.String(20), nullable=True)
    contact_point_name = db.Column(db.String(100), nullable=True)
    contact_point_email = db.Column(db.String(50), nullable=True)
    contact_point_telephone = db.Column(db.String(15), nullable=True)

    # Define other fields here

    def to_dict(self):
        """
        Change later, this returns the row created values JSON object on success
        """
        return {
            db.Column.key: getattr(self, db.Column.key)
            for db.Column.key in self.metadata.tables["assets"].columns.keys()
        }
