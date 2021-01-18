from sqlalchemy import Table, Column, Integer, String, Boolean, DateTime, func, ForeignKey

from app.config import metadata

cards = Table(
    "cards",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("text", String(length=500)),
    Column("is_crossed_out", Boolean, nullable=False, default=False),
    Column("create_date", DateTime(timezone=True), default=func.now()),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
)
