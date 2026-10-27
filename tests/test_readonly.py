"""Input wavelengths need not be writable; output arrays still must be."""

from functools import partial

import numpy as np
from numpy.testing import assert_array_equal
import pytest

import extinction


LAWS = [
    partial(extinction.ccm89, r_v=3.1),
    partial(extinction.odonnell94, r_v=3.1),
    partial(extinction.calzetti00, r_v=4.05),
    extinction.fitzpatrick99,
    extinction.Fitzpatrick99(4.0),
    extinction.fm07,
]


@pytest.mark.parametrize('law', LAWS)
@pytest.mark.parametrize('unit', ['aa', 'invum'])
@pytest.mark.parametrize('step', [1, 2, -1])
def test_readonly_wavelengths(law, unit, step):
    wave = np.array([1500., 2000., 3000., 4000., 5500., 9000.])
    if unit == 'invum':
        wave = 1.e4 / wave
    wave = wave[::step]
    expected = law(wave.copy(), 1.0, unit=unit)
    original = wave.copy()
    wave.flags.writeable = False

    actual = law(wave, 1.0, unit=unit)

    assert_array_equal(actual, expected)
    assert_array_equal(wave, original)
    assert not wave.flags.writeable
    assert actual.flags.writeable

