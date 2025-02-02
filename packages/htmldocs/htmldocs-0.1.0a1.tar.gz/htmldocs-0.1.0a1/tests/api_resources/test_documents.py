# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from htmldocs import Htmldocs, AsyncHtmldocs
from tests.utils import assert_matches_type
from htmldocs.types import (
    DocumentGenerateResponse,
    DocumentGenerateHTMLResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDocuments:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_generate(self, client: Htmldocs) -> None:
        document = client.documents.generate(
            document_id="documentId",
            props={"foo": "bar"},
        )
        assert_matches_type(DocumentGenerateResponse, document, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_generate_with_all_params(self, client: Htmldocs) -> None:
        document = client.documents.generate(
            document_id="documentId",
            props={"foo": "bar"},
            format="pdf",
            orientation="portrait",
            size="size",
        )
        assert_matches_type(DocumentGenerateResponse, document, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_generate(self, client: Htmldocs) -> None:
        response = client.documents.with_raw_response.generate(
            document_id="documentId",
            props={"foo": "bar"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = response.parse()
        assert_matches_type(DocumentGenerateResponse, document, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_generate(self, client: Htmldocs) -> None:
        with client.documents.with_streaming_response.generate(
            document_id="documentId",
            props={"foo": "bar"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = response.parse()
            assert_matches_type(DocumentGenerateResponse, document, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_generate(self, client: Htmldocs) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"):
            client.documents.with_raw_response.generate(
                document_id="",
                props={"foo": "bar"},
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_generate_html(self, client: Htmldocs) -> None:
        document = client.documents.generate_html()
        assert_matches_type(DocumentGenerateHTMLResponse, document, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_generate_html_with_all_params(self, client: Htmldocs) -> None:
        document = client.documents.generate_html(
            format="pdf",
            html="html",
            orientation="portrait",
            size="size",
            url="https://example.com",
        )
        assert_matches_type(DocumentGenerateHTMLResponse, document, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_generate_html(self, client: Htmldocs) -> None:
        response = client.documents.with_raw_response.generate_html()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = response.parse()
        assert_matches_type(DocumentGenerateHTMLResponse, document, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_generate_html(self, client: Htmldocs) -> None:
        with client.documents.with_streaming_response.generate_html() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = response.parse()
            assert_matches_type(DocumentGenerateHTMLResponse, document, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncDocuments:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_generate(self, async_client: AsyncHtmldocs) -> None:
        document = await async_client.documents.generate(
            document_id="documentId",
            props={"foo": "bar"},
        )
        assert_matches_type(DocumentGenerateResponse, document, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_generate_with_all_params(self, async_client: AsyncHtmldocs) -> None:
        document = await async_client.documents.generate(
            document_id="documentId",
            props={"foo": "bar"},
            format="pdf",
            orientation="portrait",
            size="size",
        )
        assert_matches_type(DocumentGenerateResponse, document, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_generate(self, async_client: AsyncHtmldocs) -> None:
        response = await async_client.documents.with_raw_response.generate(
            document_id="documentId",
            props={"foo": "bar"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = await response.parse()
        assert_matches_type(DocumentGenerateResponse, document, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_generate(self, async_client: AsyncHtmldocs) -> None:
        async with async_client.documents.with_streaming_response.generate(
            document_id="documentId",
            props={"foo": "bar"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = await response.parse()
            assert_matches_type(DocumentGenerateResponse, document, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_generate(self, async_client: AsyncHtmldocs) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"):
            await async_client.documents.with_raw_response.generate(
                document_id="",
                props={"foo": "bar"},
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_generate_html(self, async_client: AsyncHtmldocs) -> None:
        document = await async_client.documents.generate_html()
        assert_matches_type(DocumentGenerateHTMLResponse, document, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_generate_html_with_all_params(self, async_client: AsyncHtmldocs) -> None:
        document = await async_client.documents.generate_html(
            format="pdf",
            html="html",
            orientation="portrait",
            size="size",
            url="https://example.com",
        )
        assert_matches_type(DocumentGenerateHTMLResponse, document, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_generate_html(self, async_client: AsyncHtmldocs) -> None:
        response = await async_client.documents.with_raw_response.generate_html()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = await response.parse()
        assert_matches_type(DocumentGenerateHTMLResponse, document, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_generate_html(self, async_client: AsyncHtmldocs) -> None:
        async with async_client.documents.with_streaming_response.generate_html() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = await response.parse()
            assert_matches_type(DocumentGenerateHTMLResponse, document, path=["response"])

        assert cast(Any, response.is_closed) is True
