from . import db
from sqlalchemy import Integer, String, Column, MetaData, Table


class Assets(db.Model):
    id = Column( Integer, primary_key=True, autoincrement="auto")
    name = Column(String(100), nullable=False)
    barcode= Column(String(30), nullable=False)
    barcode_type=Column( String(4), nullable=False)
    individual_asset_reference=Column( String(30), nullable=False)
    asset_type=Column( String(30), nullable=False)
    asset_description= Column(String(256), nullable=True)
    manufacturer_name=Column( String(50), nullable=True)
    gln=Column( String(14), nullable=False)
    current_status=Column( String(20), nullable=True)
    asset_condition=Column( String(20), nullable=True)
    contact_point_name=Column( String(100), nullable=True)
    contact_point_email=Column( String(50), nullable=True)
    contact_point_telephone=Column( String(15), nullable=True)

    # Define other fields here

    def to_dict(self):
        return {Column.key: getattr(self, Column.key) for Column.key in self.metadata.tables['assets'].columns.keys()}

    # def to_dict(self):
    #     return {
    #         column.name: getattr(self, column.name)
    #         for column in self.__table__.columns
    #     }