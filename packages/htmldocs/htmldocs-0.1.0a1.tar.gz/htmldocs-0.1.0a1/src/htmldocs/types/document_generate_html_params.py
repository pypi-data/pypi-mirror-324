# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, TypedDict

__all__ = ["DocumentGenerateHTMLParams"]


class DocumentGenerateHTMLParams(TypedDict, total=False):
    format: Literal["pdf", "base64", "json"]
    """Response format.

    `pdf` returns a binary PDF file, `base64` returns the PDF encoded as base64 in
    JSON, `json` returns a URL to download the PDF. Defaults to `pdf`
    """

    html: str
    """HTML content to convert to PDF or inject into the page at the specified URL"""

    orientation: Literal["portrait", "landscape"]

    size: str
    """Page size (A3, A4, A5, letter, legal, or custom size like '8.5in 11in')"""

    url: str
    """URL of the webpage to convert to PDF or use as a base for HTML injection"""
