from typing import Literal

import numpy as np
from numpy.typing import ArrayLike, NDArray

__version__: str
__all__: list[str]

_Unit = Literal["aa", "invum"]
_Array = NDArray[np.float64]

def ccm89(
    wave: _Array,
    a_v: float,
    r_v: float,
    unit: _Unit = ...,
    out: _Array | None = ...,
) -> _Array: ...
def odonnell94(
    wave: _Array,
    a_v: float,
    r_v: float,
    unit: _Unit = ...,
    out: _Array | None = ...,
) -> _Array: ...
def calzetti00(
    wave: _Array,
    a_v: float,
    r_v: float,
    unit: _Unit = ...,
    out: _Array | None = ...,
) -> _Array: ...
def fitzpatrick99(
    wave: _Array,
    a_v: float,
    r_v: float = ...,
    unit: _Unit = ...,
) -> _Array: ...
def fm07(wave: _Array, a_v: float, unit: _Unit = ...) -> _Array: ...

class Fitzpatrick99:
    # cdef readonly in the extension: assignment raises AttributeError.
    @property
    def r_v(self) -> float: ...
    def __init__(self, r_v: float = ...) -> None: ...
    def __call__(
        self, wave: _Array, a_v: float, unit: _Unit = ...
    ) -> _Array: ...

# Unlike the wavelength arguments above, which go through typed memoryviews,
# these are plain numpy arithmetic and accept any array-like of any dtype.
def apply(
    extinction: ArrayLike, flux: ArrayLike, inplace: bool = ...
) -> _Array: ...
def remove(
    extinction: ArrayLike, flux: ArrayLike, inplace: bool = ...
) -> _Array: ...
