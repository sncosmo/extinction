"""Interstellar dust extinction functions."""

from extinction._extinction import (
    Fitzpatrick99,
    __version__,
    apply,
    calzetti00,
    ccm89,
    fitzpatrick99,
    fm07,
    odonnell94,
    remove,
)

__all__ = ['ccm89', 'odonnell94', 'Fitzpatrick99', 'fitzpatrick99', 'fm07',
           'calzetti00', 'apply', 'remove', '__version__']
