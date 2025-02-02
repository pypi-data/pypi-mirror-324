from pywander.math.linear_algebra import solve, combine_system, can_form_plane, can_form_3d_space
import numpy as np
import pytest


def test_can_form_plane():
    assert not can_form_plane(np.array((1, 2, 3)), np.array((3, 6, 9)))
    assert can_form_plane(np.array((1,0,0)), np.array((0,2,3)))

def test_can_form_3d_space():
    v1 = np.array((2, 0, 0))
    v2 = np.array((0, 2, 2))
    v3 = np.array((2, 2, 3))
    assert can_form_3d_space(v1, v2, v3)

def test_solve():
    m = np.array([
        [4, -3, 1],
        [2, 1, 3],
        [-1, 2, -5]
    ], dtype=np.dtype(float))

    b = np.array([-10, 0, 17], dtype=np.dtype(float))
    res = solve(m, b)
    assert res[0] == 1


def test_combine_system():
    m = np.array([
        [4, -3, 1],
        [2, 1, 3],
        [-1, 2, -5]
    ], dtype=np.dtype(float))

    b = np.array([-10, 0, 17], dtype=np.dtype(float))

    sys_a = combine_system(m, b)

    assert sys_a[0, 3] == -10


def test_cos():
    v1 = np.array([2, 1, 2, 3, 2, 9])
    v2 = np.array([3, 4, 2, 4, 5, 5])
    from pywander.math.linear_algebra import cos
    res = cos(v1, v2)
    assert res == pytest.approx(0.8188, abs=1e-4)
