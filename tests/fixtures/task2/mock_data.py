import pytest


@pytest.fixture
def mock_animal_data():
    return {'А': 5, 'Б': 10, 'В': 15}
