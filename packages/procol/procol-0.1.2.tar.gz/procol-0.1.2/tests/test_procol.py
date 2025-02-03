import procol
import pytest

def test_filling_prob():
    n = 10
    m = 5
    probabilities = [
        [0.2, 0.3, 0.1, 0.15, 0.25],
        [0.1, 0.2, 0.3, 0.1, 0.3],
        [0.15, 0.25, 0.2, 0.1, 0.3],
        [0.1, 0.3, 0.25, 0.2, 0.15],
        [0.2, 0.15, 0.3, 0.1, 0.25],
        [0.25, 0.1, 0.2, 0.3, 0.15],
        [0.3, 0.2, 0.1, 0.25, 0.15],
        [0.3, 0.2, 0.1, 0.15, 0.25],
        [0.25, 0.1, 0.2, 0.15, 0.3],
        [0.2, 0.3, 0.25, 0.15, 0.1],
    ]
    result = procol.filling_prob(n, m, probabilities)
    assert 0.0 <= result <= 1.0

def test_invalid_probabilities_length():
    n = 10
    m = 5
    probabilities = [
        [0.2, 0.3, 0.1, 0.15, 0.25],
        [0.1, 0.2, 0.3, 0.1, 0.3],
    ]
    with pytest.raises(ValueError):
        procol.filling_prob(n, m, probabilities)

def test_invalid_inner_probabilities_length():
    n = 10
    m = 5
    probabilities = [
        [0.2, 0.3, 0.1, 0.15, 0.25],
        [0.1, 0.2, 0.3, 0.1],
        [0.15, 0.25, 0.2, 0.1, 0.3],
        [0.1, 0.3, 0.25, 0.2, 0.15],
        [0.2, 0.15, 0.3, 0.1, 0.25],
        [0.25, 0.1, 0.2, 0.3, 0.15],
        [0.3, 0.2, 0.1, 0.25, 0.15],
        [0.3, 0.2, 0.1, 0.15, 0.25],
        [0.25, 0.1, 0.2, 0.15, 0.3],
        [0.2, 0.3, 0.25, 0.15, 0.1],
    ]
    with pytest.raises(ValueError):
        procol.filling_prob(n, m, probabilities)

def test_zero_probabilities():
    n = 5
    m = 3
    probabilities = [
        [0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0],
    ]
    result = procol.filling_prob(n, m, probabilities)
    assert result == 0.0

def test_full_probabilities():
    n = 3
    m = 2
    probabilities = [
        [1.0, 0.5],
        [0.5, 1.0],
        [1.0, 1.0],
    ]
    result = procol.filling_prob(n, m, probabilities)
    assert 0.0 <= result <= 1.0

def test_edge_case_single_event():
    n = 1
    m = 1
    probabilities = [
        [0.8],
    ]
    result = procol.filling_prob(n, m, probabilities)
    assert 0.0 <= result <= 1.0

def test_regression_0():
    result = procal.filling_prob(1,2,[[0.1, 0.2]])
    assert result >= 0

