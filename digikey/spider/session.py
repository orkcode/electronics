import asyncio
import logging
import re
import json
from curl_cffi.requests import AsyncSession, BrowserType, RequestsError, Response

from core.spider import build_proxies, parse
from parts.models import Category
from django.db import transaction


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://www.digikey.com"


async def fetch_url(session, url):
    try:
        response = await session.get(url)
        response.raise_for_status()
        logger.info(f"Fetched {url}")
        return parse(response)
    except Exception as e:
        logger.error(f"Error fetching {url}: {e}")
        return None


async def parse_categories(tree):
    categories = tree.css('*[class$="-categoryContainer"]')
    data = []

    for category in categories:
        parent_name = category.css_first('*[class$="-root-categoryLink"]').text(strip=True)
        parent_url = BASE_URL + category.css_first('*[class$="-root-categoryLink"]').attributes['href']

        subcategories = category.css('.tss-css-jir0y-NthLevelCategory-categoryListItem a')
        subcategory_list = []

        print(parent_name)

        for subcat in subcategories:
            subcat_name = subcat.text(strip=True)
            subcat_url = BASE_URL + subcat.attributes['href']
            subcat_items = int(re.search(r'\d+', subcat.css_first('.tss-css-1evuuxq-NthLevelCategory-productCount').text(strip=True)).group())

            subcategory_list.append({
                'name': subcat_name,
                'url': subcat_url,
                'items': subcat_items
            })

        data.append({
            'name': parent_name,
            'url': parent_url,
            'subcategories': subcategory_list
        })

    return data


async def save_categories_to_db(categories_data):
    categories_to_create = []
    subcategories_to_create = []

    for category in categories_data:
        parent_category, created = await Category.objects.aget_or_create(
            name=category['name'],
            parent=None
        )
        if created:
            categories_to_create.append(parent_category)

        for subcat in category['subcategories']:
            subcategories_to_create.append(
                Category(
                    name=subcat['name'],
                    parent=parent_category
                )
            )

    async with transaction.atomic():
        await Category.objects.abulk_create(categories_to_create)
        await Category.objects.abulk_create(subcategories_to_create)


async def parse_catalog():
    async with AsyncSession(impersonate='chrome') as session:
        catalog_url = BASE_URL + "/en/products"
        tree = await fetch_url(session, catalog_url)
        if tree:
            categories_data = await parse_categories(tree)
            await save_categories_to_db(categories_data)


def main():
    asyncio.run(parse_catalog())