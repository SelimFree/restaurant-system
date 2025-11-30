from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData, Enum

metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }
)

class Base(DeclarativeBase):
    metadata = metadata

# PostgreSQL enums
UserRoleEnum = Enum(
    "admin", "manager", "waiter", "cook", "customer",
    name="user_role",
    create_constraint=False
)

TableStatusEnum = Enum(
    "free", "occupied", "reserved",
    name="table_status",
    create_constraint=False
)

OrderStatusEnum = Enum(
    "created", "sent", "cooking", "ready", "served", "cancelled",
    name="order_status",
    create_constraint=False
)

OrderItemStatusEnum = Enum(
    "pending", "cooking", "ready",
    name="order_item_status",
    create_constraint=False
)