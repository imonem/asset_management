from . import db
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class Assets(db.Model):
    id : Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    barcode: Mapped[str] = mapped_column(String(30), nullable=False)
    barcode_type: Mapped[str] = mapped_column(String(4), nullable=False)
    individual_asset_reference: Mapped[str] = mapped_column(String(30), nullable=False)
    asset_type: Mapped[str] = mapped_column(String(30), nullable=False)
    asset_description: Mapped[str] = mapped_column(String(256), nullable=True)
    manufacturer_name: Mapped[str] = mapped_column(String(50), nullable=True)
    gln: Mapped[str] = mapped_column(String(14), nullable=False)
    current_status: Mapped[str] = mapped_column(String(20), nullable=True)
    asset_condition: Mapped[str] = mapped_column(String(20), nullable=True)
    contact_point_name: Mapped[str] = mapped_column(String(100), nullable=True)
    contact_point_email: Mapped[str] = mapped_column(String(50), nullable=True)
    contact_point_telephone: Mapped[str] = mapped_column(String(15), nullable=True)

    # Define other fields here