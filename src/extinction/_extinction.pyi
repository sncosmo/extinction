from typing import Literal

import numpy as np
from numpy.typing import NDArray

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
    r_v: float
    def __init__(self, r_v: float = ...) -> None: ...
    def __call__(
        self, wave: _Array, a_v: float, unit: _Unit = ...
    ) -> _Array: ...

def apply(
    extinction: _Array, flux: _Array, inplace: bool = ...
) -> _Array: ...
def remove(
    extinction: _Array, flux: _Array, inplace: bool = ...
) -> _Array: ...
