"""Input wavelengths need not be writable; output arrays still must be."""

from functools import partial

import numpy as np
import pytest
from numpy.testing import assert_array_equal

import extinction

LAWS = [
    partial(extinction.ccm89, r_v=3.1),
    partial(extinction.odonnell94, r_v=3.1),
    partial(extinction.calzetti00, r_v=4.05),
    extinction.fitzpatrick99,
    extinction.Fitzpatrick99(4.0),
    extinction.fm07,
]


@pytest.mark.parametrize("law", LAWS)
@pytest.mark.parametrize("unit", ["aa", "invum"])
@pytest.mark.parametrize("step", [1, 2, -1])
def test_readonly_wavelengths(law, unit, step):
    wave = np.array([1500.0, 2000.0, 3000.0, 4000.0, 5500.0, 9000.0])
    if unit == "invum":
        wave = 1.0e4 / wave
    wave = wave[::step]
    expected = law(wave.copy(), 1.0, unit=unit)
    original = wave.copy()
    wave.flags.writeable = False

    actual = law(wave, 1.0, unit=unit)

    assert_array_equal(actual, expected)
    assert_array_equal(wave, original)
    assert not wave.flags.writeable
    assert actual.flags.writeable
