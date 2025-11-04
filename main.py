from datetime import date, datetime, timedelta
from parser import parse_page_links
from typing import List
import asyncio
import aiohttp

import requests
from pandas import DataFrame

from base import get_session
from models import ExchangeProduct
from utils import extract_table, filter_needed_columns, get_data


def df_to_models(df: DataFrame, current_date = date.today()) -> List[ExchangeProduct]:
    products: List[ExchangeProduct] = []

    for _, row in df.iterrows():
        code = str(row["Код\nИнструмента"]).strip()
        oil_id = code[:4]
        delivery_basis_id = code[4:7]
        delivery_type_id = code[-1]

        product = ExchangeProduct(
            exchange_product_id=code,
            exchange_product_name=str(row["Наименование\nИнструмента"]).strip(),
            oil_id=oil_id,
            delivery_basis_id=delivery_basis_id,
            delivery_basis_name=str(row["Базис\nпоставки"]).strip(),
            delivery_type_id=delivery_type_id,
            volume=float(row["Объем\nДоговоров\nв единицах\nизмерения"]),
            total=float(row["Обьем\nДоговоров,\nруб."]),
            count=int(row["Количество\nДоговоров,\nшт."]),
            date=current_date,
            created_on=datetime.now().date(),
            updated_on=datetime.now().date(),
        )
        products.append(product)
    return products


async def save_to_db(products: List[ExchangeProduct]) -> None:
    session_gen = get_session()
    session = next(session_gen)

    session.add_all(products)
    session.commit()
    session.close()


if __name__ == "__main__":

    url = "https://spimex.com/markets/oil_products/trades/results/"
    response = requests.get(url)
    end_date = date.today()
    start_date = end_date - timedelta(days=730)

    links = parse_page_links(response.content, start_date, end_date, url)

    for link in links:
        file_url, date = link
        table = get_data([file_url, date])
        table = extract_table(table)
        table = filter_needed_columns(table)
        products = df_to_models(table)
        save_to_db(products)
