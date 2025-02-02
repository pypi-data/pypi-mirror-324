# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, Dict, cast
from typing_extensions import Literal

import httpx

from ..types import document_generate_params, document_generate_html_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.document_generate_response import DocumentGenerateResponse
from ..types.document_generate_html_response import DocumentGenerateHTMLResponse

__all__ = ["DocumentsResource", "AsyncDocumentsResource"]


class DocumentsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DocumentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/htmldocs-js/htmldocs-py#accessing-raw-response-data-eg-headers
        """
        return DocumentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DocumentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/htmldocs-js/htmldocs-py#with_streaming_response
        """
        return DocumentsResourceWithStreamingResponse(self)

    def generate(
        self,
        document_id: str,
        *,
        props: Dict[str, object],
        format: Literal["pdf", "base64", "json"] | NotGiven = NOT_GIVEN,
        orientation: Literal["portrait", "landscape"] | NotGiven = NOT_GIVEN,
        size: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DocumentGenerateResponse:
        """
        Generates a PDF document from a published document template.

        Args:
          props: Props to pass to the document component

          format: Response format. `pdf` returns a binary PDF file, `base64` returns the PDF
              encoded as base64 in JSON, `json` returns a URL to download the PDF. Defaults to
              `pdf`

          size: Page size (A3, A4, A5, letter, legal, or custom size like '8.5in 11in')

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not document_id:
            raise ValueError(f"Expected a non-empty value for `document_id` but received {document_id!r}")
        return cast(
            DocumentGenerateResponse,
            self._post(
                f"/api/documents/{document_id}",
                body=maybe_transform(
                    {
                        "props": props,
                        "format": format,
                        "orientation": orientation,
                        "size": size,
                    },
                    document_generate_params.DocumentGenerateParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, DocumentGenerateResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def generate_html(
        self,
        *,
        format: Literal["pdf", "base64", "json"] | NotGiven = NOT_GIVEN,
        html: str | NotGiven = NOT_GIVEN,
        orientation: Literal["portrait", "landscape"] | NotGiven = NOT_GIVEN,
        size: str | NotGiven = NOT_GIVEN,
        url: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DocumentGenerateHTMLResponse:
        """Generates a PDF document from raw HTML content and/or a URL.

        If both are
        provided, the HTML content will be injected into the page at the specified URL.

        Args:
          format: Response format. `pdf` returns a binary PDF file, `base64` returns the PDF
              encoded as base64 in JSON, `json` returns a URL to download the PDF. Defaults to
              `pdf`

          html: HTML content to convert to PDF or inject into the page at the specified URL

          size: Page size (A3, A4, A5, letter, legal, or custom size like '8.5in 11in')

          url: URL of the webpage to convert to PDF or use as a base for HTML injection

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return cast(
            DocumentGenerateHTMLResponse,
            self._post(
                "/api/generate",
                body=maybe_transform(
                    {
                        "format": format,
                        "html": html,
                        "orientation": orientation,
                        "size": size,
                        "url": url,
                    },
                    document_generate_html_params.DocumentGenerateHTMLParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, DocumentGenerateHTMLResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )


class AsyncDocumentsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDocumentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/htmldocs-js/htmldocs-py#accessing-raw-response-data-eg-headers
        """
        return AsyncDocumentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDocumentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/htmldocs-js/htmldocs-py#with_streaming_response
        """
        return AsyncDocumentsResourceWithStreamingResponse(self)

    async def generate(
        self,
        document_id: str,
        *,
        props: Dict[str, object],
        format: Literal["pdf", "base64", "json"] | NotGiven = NOT_GIVEN,
        orientation: Literal["portrait", "landscape"] | NotGiven = NOT_GIVEN,
        size: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DocumentGenerateResponse:
        """
        Generates a PDF document from a published document template.

        Args:
          props: Props to pass to the document component

          format: Response format. `pdf` returns a binary PDF file, `base64` returns the PDF
              encoded as base64 in JSON, `json` returns a URL to download the PDF. Defaults to
              `pdf`

          size: Page size (A3, A4, A5, letter, legal, or custom size like '8.5in 11in')

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not document_id:
            raise ValueError(f"Expected a non-empty value for `document_id` but received {document_id!r}")
        return cast(
            DocumentGenerateResponse,
            await self._post(
                f"/api/documents/{document_id}",
                body=await async_maybe_transform(
                    {
                        "props": props,
                        "format": format,
                        "orientation": orientation,
                        "size": size,
                    },
                    document_generate_params.DocumentGenerateParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, DocumentGenerateResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    async def generate_html(
        self,
        *,
        format: Literal["pdf", "base64", "json"] | NotGiven = NOT_GIVEN,
        html: str | NotGiven = NOT_GIVEN,
        orientation: Literal["portrait", "landscape"] | NotGiven = NOT_GIVEN,
        size: str | NotGiven = NOT_GIVEN,
        url: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DocumentGenerateHTMLResponse:
        """Generates a PDF document from raw HTML content and/or a URL.

        If both are
        provided, the HTML content will be injected into the page at the specified URL.

        Args:
          format: Response format. `pdf` returns a binary PDF file, `base64` returns the PDF
              encoded as base64 in JSON, `json` returns a URL to download the PDF. Defaults to
              `pdf`

          html: HTML content to convert to PDF or inject into the page at the specified URL

          size: Page size (A3, A4, A5, letter, legal, or custom size like '8.5in 11in')

          url: URL of the webpage to convert to PDF or use as a base for HTML injection

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return cast(
            DocumentGenerateHTMLResponse,
            await self._post(
                "/api/generate",
                body=await async_maybe_transform(
                    {
                        "format": format,
                        "html": html,
                        "orientation": orientation,
                        "size": size,
                        "url": url,
                    },
                    document_generate_html_params.DocumentGenerateHTMLParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, DocumentGenerateHTMLResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )


class DocumentsResourceWithRawResponse:
    def __init__(self, documents: DocumentsResource) -> None:
        self._documents = documents

        self.generate = to_raw_response_wrapper(
            documents.generate,
        )
        self.generate_html = to_raw_response_wrapper(
            documents.generate_html,
        )


class AsyncDocumentsResourceWithRawResponse:
    def __init__(self, documents: AsyncDocumentsResource) -> None:
        self._documents = documents

        self.generate = async_to_raw_response_wrapper(
            documents.generate,
        )
        self.generate_html = async_to_raw_response_wrapper(
            documents.generate_html,
        )


class DocumentsResourceWithStreamingResponse:
    def __init__(self, documents: DocumentsResource) -> None:
        self._documents = documents

        self.generate = to_streamed_response_wrapper(
            documents.generate,
        )
        self.generate_html = to_streamed_response_wrapper(
            documents.generate_html,
        )


class AsyncDocumentsResourceWithStreamingResponse:
    def __init__(self, documents: AsyncDocumentsResource) -> None:
        self._documents = documents

        self.generate = async_to_streamed_response_wrapper(
            documents.generate,
        )
        self.generate_html = async_to_streamed_response_wrapper(
            documents.generate_html,
        )
