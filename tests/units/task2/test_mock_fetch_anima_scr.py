import csv
import os

import pytest

from src.task2.solution import fetch_animal_counts


pytestmark = pytest.mark.asyncio


async def test_fetch_animal_counts(monkeypatch):
    csv_path = 'beasts.csv'

    await fetch_animal_counts()

    with open(csv_path, encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
        assert len(rows) == 29

    os.remove(csv_path)
