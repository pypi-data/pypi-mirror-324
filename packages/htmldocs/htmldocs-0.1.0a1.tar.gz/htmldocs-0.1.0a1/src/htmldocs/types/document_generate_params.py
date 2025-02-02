# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Literal, Required, TypedDict

__all__ = ["DocumentGenerateParams"]


class DocumentGenerateParams(TypedDict, total=False):
    props: Required[Dict[str, object]]
    """Props to pass to the document component"""

    format: Literal["pdf", "base64", "json"]
    """Response format.

    `pdf` returns a binary PDF file, `base64` returns the PDF encoded as base64 in
    JSON, `json` returns a URL to download the PDF. Defaults to `pdf`
    """

    orientation: Literal["portrait", "landscape"]

    size: str
    """Page size (A3, A4, A5, letter, legal, or custom size like '8.5in 11in')"""
