from sqlalchemy import Table, Column, Integer, String, DateTime, func, ForeignKey

from app.config import metadata

refresh_token = Table(
    "refresh_tokens",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("token", String(length=300), nullable=False, index=True),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("create_date", DateTime(timezone=True), default=func.now()),
)
