from datetime import date, datetime
from typing import Optional

from sqlalchemy import Date, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from base import Base


class ExchangeProduct(Base):
    __tablename__ = "exchange_products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    exchange_product_id: Mapped[str] = mapped_column(
        String, nullable=False, unique=True
    )
    exchange_product_name: Mapped[str] = mapped_column(String, nullable=False)

    oil_id: Mapped[str] = mapped_column(
        String(4), nullable=False
    )
    delivery_basis_id: Mapped[str] = mapped_column(
        String(3), nullable=False
    )
    delivery_basis_name: Mapped[str] = mapped_column(String, nullable=False)
    delivery_type_id: Mapped[str] = mapped_column(
        String(1), nullable=False
    )

    volume: Mapped[Optional[float]] = mapped_column(Float)
    total: Mapped[Optional[float]] = mapped_column(Float)
    count: Mapped[Optional[int]] = mapped_column(Integer)

    date: Mapped[date] = mapped_column(Date, nullable=False)

    created_on: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_on: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self) -> str:
        return (
            f"<ExchangeProduct(id={self.id}, name={self.exchange_product_name!r}, "
            f"date={self.date}, exchange_product_id={self.exchange_product_id!r})>"
        )
