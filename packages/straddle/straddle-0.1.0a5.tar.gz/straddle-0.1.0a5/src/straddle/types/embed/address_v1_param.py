# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["AddressV1Param"]


class AddressV1Param(TypedDict, total=False):
    city: Optional[str]
    """City, district, suburb, town, or village."""

    country: Optional[str]
    """The country of the address, in ISO 3166-1 alpha-2 format."""

    line1: Optional[str]
    """Primary address line (e.g., street, PO Box)."""

    line2: Optional[str]
    """Secondary address line (e.g., apartment, suite, unit, or building)."""

    postal_code: Optional[str]
    """Postal or ZIP code."""

    state: Optional[str]
    """Two-letter state code."""
