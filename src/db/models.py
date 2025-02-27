from sqlalchemy import BigInteger, DateTime, String, Float
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(Base):
    __tablename__ = "users"

    id_user: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[str] = mapped_column(String(length=64), nullable=True)


class Bill(Base):
    __tablename__ = "bills"

    fd: Mapped[int] = mapped_column(BigInteger)  # ФД
    fn: Mapped[int] = mapped_column(BigInteger)  # ФН
    fp: Mapped[str] = mapped_column(String(length=64))  # ФП
    sum: Mapped[int] = mapped_column(BigInteger)  # Сумма
    date: Mapped[str] = mapped_column(DateTime)  # Дата


class Product(Base):
    __tablename__ = "products"

    idpk_bill: Mapped[int] = mapped_column(BigInteger)  # Идентификатор чека
    name: Mapped[str] = mapped_column(String(length=500))  # Название товара
    price: Mapped[int] = mapped_column(BigInteger)  # Цена
    count: Mapped[float] = mapped_column(Float)  # Количество
    sum: Mapped[float] = mapped_column(Float)  # Сумма


class Text(Base):
    __tablename__ = "texts"

    name: Mapped[str] = mapped_column(String(length=100))  # Название текста
    text: Mapped[str] = mapped_column(
        String(length=4096), default="текст не задан"
    )  # Текст


class Button(Base):
    __tablename__ = "buttons"

    name: Mapped[str] = mapped_column(String(length=100))  # Название кнопки
    text: Mapped[str] = mapped_column(
        String(length=64), default="кнопка"
    )  # Текст кнопки


class BlackList(Base):
    __tablename__ = "blacklist"

    id_user: Mapped[int] = mapped_column(BigInteger)  # Идентификатор пользователя


class Value(Base):
    __tablename__ = "values"

    name: Mapped[str] = mapped_column(String(length=100))  # Название значения
    value_int: Mapped[int] = mapped_column(BigInteger, default=0)  # Значение целое
    value_str: Mapped[str] = mapped_column(
        String(length=4096), default="не установлено"
    )  # Значение строка
