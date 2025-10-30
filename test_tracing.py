import pytest
from numpy import pi, nan, isnan
from tracingpoint import calcul_image, preparation_fonction, creation_segments


def test_preparation_fonction():
    assert preparation_fonction("2x") == "2*x"
    assert preparation_fonction("3x+5x") == "3*x+5*x"

    assert preparation_fonction("2(x+1)") == "2*(x+1)"
    assert preparation_fonction("(x+1)3") == "(x+1)*3"


def test_evaluation_fonction():
    assert calcul_image(preparation_fonction("2x+4"), 3) == 10
    assert calcul_image(preparation_fonction("x**2"), 4) == 16
    assert calcul_image(preparation_fonction("x**3-2x+1"), 2) == 5

    resultat = calcul_image(preparation_fonction("sin(x)"), pi / 2)
    assert abs(resultat - 1.0) < 0.0001

    with pytest.raises(ZeroDivisionError):
        calcul_image(preparation_fonction("1/x"), 0)


def test_creation_segments():
    X = [1, 2, 3, 4, 5, 6]
    Y = [1.0, 1.1, nan, 4.0, 4.1, 4.2]

    segments = creation_segments(X, Y)

    assert len(segments) == 2
    assert segments[0] == ([1, 2], [1.0, 1.1])
    assert segments[1] == ([4, 5, 6], [4.0, 4.1, 4.2])
