import pytest

from app import Figure


@pytest.mark.parametrize("figure_type", Figure.FIGURES)
def test_get_angles_without_assert(figure_type):
    Figure(figure_type, 1).get_angles


def test_fallback_without_assert():
    figure = Figure("квадрат", 1)
    figure.type = "коло"
    figure.get_angles
