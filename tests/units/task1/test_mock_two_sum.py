import pytest
from src.task1.solution import sum_two


def test_valid_arguments():
    """Тест: корректные аргументы вызывают функцию без ошибок."""
    assert sum_two(1, 2) == 3


def test_invalid_argument_type():
    """Тест: некорректный тип аргументов вызывает TypeError."""
    with pytest.raises(TypeError):
        sum_two(1, "2")

