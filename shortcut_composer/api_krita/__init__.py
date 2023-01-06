"""
Wraps krita api, ensuring PEP8 compatibility, proper typing and enums.

Main wrapper `Krita` can return wrappers to other elements of the
interface. This package has to be independent of other extension
packages.

Other api elements that require importing from other packages are
available here so that the imports to omit unresolved warnings there.
"""

from krita import Extension, QMdiArea
from .core_api import Krita

__all__ = ["Extension", "QMdiArea", "Krita"]