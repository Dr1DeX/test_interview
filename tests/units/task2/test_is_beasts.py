import os
from pathlib import Path

from src.task2.solution import save_to_csv


def test_save_to_csv(monkeypatch, mock_animal_data):
    csv_path = 'beasts.csv'

    save_to_csv(mock_animal_data)

    assert Path(csv_path).exists()

    os.remove(csv_path)
