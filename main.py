import aiohttp
import asyncio
from datetime import date, datetime, timedelta
from typing import List
from pandas import DataFrame

from parser import parse_page_links
from base import get_async_session
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

async def fetch_page(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()


async def get_raw_data(file_url: str, date_: date):
    content = get_data(file_url)
    table = extract_table(content)
    table = filter_needed_columns(table)
    return df_to_models(table, date_)


async def save_to_db(products: List[ExchangeProduct]):
    async with get_async_session() as session:
        session.add_all(products)
        await session.commit()


async def process_link(link):
    file_url, file_date = link
    products = await get_raw_data(file_url, file_date)
    await save_to_db(products)


async def main():
    url = "https://spimex.com/markets/oil_products/trades/results/"
    html = await fetch_page(url)

    end_date = date.today()
    start_date = end_date - timedelta(days=730)
    links = parse_page_links(html, start_date, end_date, url)

    sem = asyncio.Semaphore(5)
    async def limited(link):
        async with sem:
            await process_link(link)

    await asyncio.gather(*(limited(link) for link in links))


if __name__ == "__main__":
    asyncio.run(main())
