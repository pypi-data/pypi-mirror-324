# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["AddressV1"]


class AddressV1(BaseModel):
    city: Optional[str] = None
    """City, district, suburb, town, or village."""

    country: Optional[str] = None
    """The country of the address, in ISO 3166-1 alpha-2 format."""

    line1: Optional[str] = None
    """Primary address line (e.g., street, PO Box)."""

    line2: Optional[str] = None
    """Secondary address line (e.g., apartment, suite, unit, or building)."""

    postal_code: Optional[str] = None
    """Postal or ZIP code."""

    state: Optional[str] = None
    """Two-letter state code."""
