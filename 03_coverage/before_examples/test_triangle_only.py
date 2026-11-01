from app import Figure


def test_triangle_angles():
    assert Figure("трикутник", 1).get_angles == 3
