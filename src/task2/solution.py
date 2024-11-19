import asyncio
import csv
import logging

from playwright.async_api import async_playwright


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def fetch_animal_counts():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        alpha = [chr(i) for i in range(ord('А'), ord('Я') + 1) if chr(i) != 'Ё']

        anima_counts = {}

        base_url = (
            'https://ru.wikipedia.org/w/index.php?title=Категория:Животные_по_алфавиту&pagefrom={'
            'letter}#mw-pages'
        )

        for letter in alpha:
            url = base_url.format(letter=letter)
            logger.info(f'Fetching: {url}')

            await page.goto(url)

            await page.wait_for_selector("#mw-pages .mw-category-group a")

            links = await page.query_selector_all("#mw-pages .mw-category-group a")

            for link in links:
                title = await link.get_attribute('title')
                if title:
                    first_letter = title.split(':')[-1][0].upper()

                    if 'А' <= first_letter <= 'Я':
                        if first_letter not in anima_counts:
                            anima_counts[first_letter] = 0
                        anima_counts[first_letter] += 1

        await browser.close()

        save_to_csv(anima_counts)


def save_to_csv(animal_counts: dict) -> None:
    with open('beasts.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for letter, count in sorted(animal_counts.items()):
            writer.writerow([letter, count])


if __name__ == '__main__':
    asyncio.run(fetch_animal_counts())
