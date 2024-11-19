import csv
import os
from unittest.mock import (
    AsyncMock,
    MagicMock,
    patch,
)

import pytest

from src.task2.solution import fetch_animal_counts


pytestmark = pytest.mark.asyncio

MOCK_ANIMALS = [
    "Аист",
    "Акула",
    "Антилопа",
    "Баран",
    "Бегемот",
    "Белка",
    "Верблюд",
    "Волк",
    "Воробей",
    "Голубь",
    "Гусь",
    "Дельфин",
    "Енот",
    "Жираф",
    "Заяц",
    "Индюк",
    "Кит",
    "Курица",
    "Лев",
    "Лиса",
    "Медведь",
    "Мышь",
    "Носорог",
    "Обезьяна",
    "Орел",
    "Панда",
    "Попугай",
    "Рысь",
    "Слон",
]


async def mock_query_selector_all(selector):
    return [
        MagicMock(get_attribute=AsyncMock(return_value=animal))
        for animal in MOCK_ANIMALS
    ]


@patch("src.task2.solution.async_playwright")
async def test_fetch_animal_counts(mock_playwright):
    csv_path = "beasts.csv"

    mock_browser = MagicMock()
    mock_browser.close = AsyncMock()
    mock_page = MagicMock()

    # Замоканные асинхронные методы
    mock_page.goto = AsyncMock()
    mock_page.query_selector_all = AsyncMock(side_effect=mock_query_selector_all)
    mock_page.wait_for_selector = AsyncMock()
    mock_browser.new_page = AsyncMock(return_value=mock_page)

    # Замокать Playwright
    mock_playwright.return_value.__aenter__.return_value.chromium.launch = AsyncMock(
        return_value=mock_browser,
    )

    await fetch_animal_counts()

    with open(csv_path, encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)
        assert len(rows) == 17

    os.remove(csv_path)
