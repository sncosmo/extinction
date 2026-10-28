"""The documented output array must receive and return the calculated values."""

from functools import partial

import numpy as np
import pytest
from numpy.testing import assert_array_equal

import extinction

LAWS = [
    partial(extinction.ccm89, r_v=3.1),
    partial(extinction.odonnell94, r_v=3.1),
    partial(extinction.calzetti00, r_v=4.05),
]


@pytest.mark.parametrize("law", LAWS)
@pytest.mark.parametrize("unit", ["aa", "invum"])
@pytest.mark.parametrize("step", [1, 2, -1])
def test_out(law, unit, step):
    wave = np.array([2000.0, 4000.0, 8000.0])
    if unit == "invum":
        wave = 1.0e4 / wave
    original = wave.copy()
    expected = law(wave, 1.0, unit=unit)
    backing = np.full(wave.size * abs(step), -1.0)
    out = backing[::step]

    assert law(wave, 1.0, unit=unit, out=out) is out

    assert_array_equal(out, expected)
    assert_array_equal(wave, original)
    if step == 2:
        assert_array_equal(backing[1::2], -1.0)


@pytest.mark.parametrize("law", LAWS)
@pytest.mark.parametrize("unit", ["aa", "invum"])
def test_out_can_alias_wavelengths(law, unit):
    wave = np.array([2000.0, 4000.0, 8000.0])
    if unit == "invum":
        wave = 1.0e4 / wave
    expected = law(wave.copy(), 1.0, unit=unit)

    assert law(wave, 1.0, unit=unit, out=wave) is wave
    assert_array_equal(wave, expected)


@pytest.mark.parametrize("law", LAWS)
@pytest.mark.parametrize("size", [0, 2, 4])
def test_out_wrong_length(law, size):
    # The loop writes len(wave) values without bounds checks, so this check
    # must not be an assert, which `python -O` skips.
    wave = np.array([2000.0, 4000.0, 8000.0])
    backing = np.full(8, -1.0)

    with pytest.raises(ValueError, match="same length as wave"):
        law(wave, 1.0, out=backing[:size])

    assert_array_equal(backing, -1.0)


@pytest.mark.parametrize("law", LAWS)
@pytest.mark.parametrize(
    ("shape", "dtype"),
    [((1, 3), np.float64), (3, np.float32), (3, [("a", np.float64)])],
    ids=["2d", "float32", "structured"],
)
def test_out_wrong_ndim_or_dtype(law, shape, dtype):
    wave = np.array([2000.0, 4000.0, 8000.0])

    with pytest.raises(ValueError, match="out must"):
        law(wave, 1.0, out=np.zeros(shape, dtype=dtype))
