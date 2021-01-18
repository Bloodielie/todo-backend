from sqlalchemy import Table, Column, Integer, String, DateTime, func

from app.config import metadata

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String(length=100), unique=True, nullable=False),
    Column("password", String(length=100), nullable=False),
    Column("user_name", String(length=50)),
    Column("create_date", DateTime(timezone=True), default=func.now()),
)
