# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from objective import Objective, AsyncObjective
from tests.utils import assert_matches_type
from objective.types import (
    IndexGetResponse,
    IndexListResponse,
    IndexCreateResponse,
    IndexDeleteResponse,
    IndexSearchResponse,
    IndexStatusResponse,
    IndexFinetuneResponse,
    IndexStatusByTypeResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestIndexes:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Objective) -> None:
        index = client.indexes.create(
            configuration={"fields": {"searchable": {"allow": ["string"]}}},
        )
        assert_matches_type(IndexCreateResponse, index, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Objective) -> None:
        index = client.indexes.create(
            configuration={
                "fields": {
                    "searchable": {"allow": ["string"]},
                    "crawlable": {"allow": ["string"]},
                    "fast_filters": ["string"],
                    "filterable": {"allow": ["string"]},
                    "segment_delimiter": {"foo": "bar"},
                    "types": {"foo": "string"},
                },
                "index_type": {
                    "name": "multimodal",
                    "finetuning": {
                        "base_index_id": "base_index_id",
                        "feedback": [
                            {
                                "query": "query",
                                "label": "GREAT",
                                "object_id": "object_id",
                            }
                        ],
                    },
                    "highlights": {"text": True},
                    "version": "version",
                },
            },
        )
        assert_matches_type(IndexCreateResponse, index, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Objective) -> None:
        response = client.indexes.with_raw_response.create(
            configuration={"fields": {"searchable": {"allow": ["string"]}}},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        index = response.parse()
        assert_matches_type(IndexCreateResponse, index, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Objective) -> None:
        with client.indexes.with_streaming_response.create(
            configuration={"fields": {"searchable": {"allow": ["string"]}}},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            index = response.parse()
            assert_matches_type(IndexCreateResponse, index, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_list(self, client: Objective) -> None:
        index = client.indexes.list()
        assert_matches_type(IndexListResponse, index, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Objective) -> None:
        response = client.indexes.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        index = response.parse()
        assert_matches_type(IndexListResponse, index, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Objective) -> None:
        with client.indexes.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            index = response.parse()
            assert_matches_type(IndexListResponse, index, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Objective) -> None:
        index = client.indexes.delete(
            "idx_1234",
        )
        assert_matches_type(IndexDeleteResponse, index, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Objective) -> None:
        response = client.indexes.with_raw_response.delete(
            "idx_1234",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        index = response.parse()
        assert_matches_type(IndexDeleteResponse, index, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Objective) -> None:
        with client.indexes.with_streaming_response.delete(
            "idx_1234",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            index = response.parse()
            assert_matches_type(IndexDeleteResponse, index, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Objective) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `index_id` but received ''"):
            client.indexes.with_raw_response.delete(
                "",
            )

    @parametrize
    def test_method_finetune(self, client: Objective) -> None:
        index = client.indexes.finetune(
            index_id="idx_123",
            feedback=[{"query": "query"}],
        )
        assert_matches_type(IndexFinetuneResponse, index, path=["response"])

    @parametrize
    def test_raw_response_finetune(self, client: Objective) -> None:
        response = client.indexes.with_raw_response.finetune(
            index_id="idx_123",
            feedback=[{"query": "query"}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        index = response.parse()
        assert_matches_type(IndexFinetuneResponse, index, path=["response"])

    @parametrize
    def test_streaming_response_finetune(self, client: Objective) -> None:
        with client.indexes.with_streaming_response.finetune(
            index_id="idx_123",
            feedback=[{"query": "query"}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            index = response.parse()
            assert_matches_type(IndexFinetuneResponse, index, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_finetune(self, client: Objective) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `index_id` but received ''"):
            client.indexes.with_raw_response.finetune(
                index_id="",
                feedback=[{"query": "query"}],
            )

    @parametrize
    def test_method_get(self, client: Objective) -> None:
        index = client.indexes.get(
            "idx_1234",
        )
        assert_matches_type(IndexGetResponse, index, path=["response"])

    @parametrize
    def test_raw_response_get(self, client: Objective) -> None:
        response = client.indexes.with_raw_response.get(
            "idx_1234",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        index = response.parse()
        assert_matches_type(IndexGetResponse, index, path=["response"])

    @parametrize
    def test_streaming_response_get(self, client: Objective) -> None:
        with client.indexes.with_streaming_response.get(
            "idx_1234",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            index = response.parse()
            assert_matches_type(IndexGetResponse, index, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_get(self, client: Objective) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `index_id` but received ''"):
            client.indexes.with_raw_response.get(
                "",
            )

    @parametrize
    def test_method_search(self, client: Objective) -> None:
        index = client.indexes.search(
            index_id="idx_123",
        )
        assert_matches_type(IndexSearchResponse, index, path=["response"])

    @parametrize
    def test_method_search_with_all_params(self, client: Objective) -> None:
        index = client.indexes.search(
            index_id="idx_123",
            filter_query="filter_query",
            limit=0,
            object_fields="object_fields",
            offset=0,
            query="query",
            ranking_expr="ranking_expr",
            relevance_cutoff="relevance_cutoff",
            result_fields="result_fields",
        )
        assert_matches_type(IndexSearchResponse, index, path=["response"])

    @parametrize
    def test_raw_response_search(self, client: Objective) -> None:
        response = client.indexes.with_raw_response.search(
            index_id="idx_123",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        index = response.parse()
        assert_matches_type(IndexSearchResponse, index, path=["response"])

    @parametrize
    def test_streaming_response_search(self, client: Objective) -> None:
        with client.indexes.with_streaming_response.search(
            index_id="idx_123",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            index = response.parse()
            assert_matches_type(IndexSearchResponse, index, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_search(self, client: Objective) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `index_id` but received ''"):
            client.indexes.with_raw_response.search(
                index_id="",
            )

    @parametrize
    def test_method_status(self, client: Objective) -> None:
        index = client.indexes.status(
            "idx_1234",
        )
        assert_matches_type(IndexStatusResponse, index, path=["response"])

    @parametrize
    def test_raw_response_status(self, client: Objective) -> None:
        response = client.indexes.with_raw_response.status(
            "idx_1234",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        index = response.parse()
        assert_matches_type(IndexStatusResponse, index, path=["response"])

    @parametrize
    def test_streaming_response_status(self, client: Objective) -> None:
        with client.indexes.with_streaming_response.status(
            "idx_1234",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            index = response.parse()
            assert_matches_type(IndexStatusResponse, index, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_status(self, client: Objective) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `index_id` but received ''"):
            client.indexes.with_raw_response.status(
                "",
            )

    @parametrize
    def test_method_status_by_type(self, client: Objective) -> None:
        index = client.indexes.status_by_type(
            index_status_type="UPLOADED",
            index_id="idx_123",
        )
        assert_matches_type(IndexStatusByTypeResponse, index, path=["response"])

    @parametrize
    def test_raw_response_status_by_type(self, client: Objective) -> None:
        response = client.indexes.with_raw_response.status_by_type(
            index_status_type="UPLOADED",
            index_id="idx_123",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        index = response.parse()
        assert_matches_type(IndexStatusByTypeResponse, index, path=["response"])

    @parametrize
    def test_streaming_response_status_by_type(self, client: Objective) -> None:
        with client.indexes.with_streaming_response.status_by_type(
            index_status_type="UPLOADED",
            index_id="idx_123",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            index = response.parse()
            assert_matches_type(IndexStatusByTypeResponse, index, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_status_by_type(self, client: Objective) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `index_id` but received ''"):
            client.indexes.with_raw_response.status_by_type(
                index_status_type="UPLOADED",
                index_id="",
            )


class TestAsyncIndexes:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncObjective) -> None:
        index = await async_client.indexes.create(
            configuration={"fields": {"searchable": {"allow": ["string"]}}},
        )
        assert_matches_type(IndexCreateResponse, index, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncObjective) -> None:
        index = await async_client.indexes.create(
            configuration={
                "fields": {
                    "searchable": {"allow": ["string"]},
                    "crawlable": {"allow": ["string"]},
                    "fast_filters": ["string"],
                    "filterable": {"allow": ["string"]},
                    "segment_delimiter": {"foo": "bar"},
                    "types": {"foo": "string"},
                },
                "index_type": {
                    "name": "multimodal",
                    "finetuning": {
                        "base_index_id": "base_index_id",
                        "feedback": [
                            {
                                "query": "query",
                                "label": "GREAT",
                                "object_id": "object_id",
                            }
                        ],
                    },
                    "highlights": {"text": True},
                    "version": "version",
                },
            },
        )
        assert_matches_type(IndexCreateResponse, index, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncObjective) -> None:
        response = await async_client.indexes.with_raw_response.create(
            configuration={"fields": {"searchable": {"allow": ["string"]}}},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        index = await response.parse()
        assert_matches_type(IndexCreateResponse, index, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncObjective) -> None:
        async with async_client.indexes.with_streaming_response.create(
            configuration={"fields": {"searchable": {"allow": ["string"]}}},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            index = await response.parse()
            assert_matches_type(IndexCreateResponse, index, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_list(self, async_client: AsyncObjective) -> None:
        index = await async_client.indexes.list()
        assert_matches_type(IndexListResponse, index, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncObjective) -> None:
        response = await async_client.indexes.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        index = await response.parse()
        assert_matches_type(IndexListResponse, index, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncObjective) -> None:
        async with async_client.indexes.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            index = await response.parse()
            assert_matches_type(IndexListResponse, index, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncObjective) -> None:
        index = await async_client.indexes.delete(
            "idx_1234",
        )
        assert_matches_type(IndexDeleteResponse, index, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncObjective) -> None:
        response = await async_client.indexes.with_raw_response.delete(
            "idx_1234",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        index = await response.parse()
        assert_matches_type(IndexDeleteResponse, index, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncObjective) -> None:
        async with async_client.indexes.with_streaming_response.delete(
            "idx_1234",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            index = await response.parse()
            assert_matches_type(IndexDeleteResponse, index, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncObjective) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `index_id` but received ''"):
            await async_client.indexes.with_raw_response.delete(
                "",
            )

    @parametrize
    async def test_method_finetune(self, async_client: AsyncObjective) -> None:
        index = await async_client.indexes.finetune(
            index_id="idx_123",
            feedback=[{"query": "query"}],
        )
        assert_matches_type(IndexFinetuneResponse, index, path=["response"])

    @parametrize
    async def test_raw_response_finetune(self, async_client: AsyncObjective) -> None:
        response = await async_client.indexes.with_raw_response.finetune(
            index_id="idx_123",
            feedback=[{"query": "query"}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        index = await response.parse()
        assert_matches_type(IndexFinetuneResponse, index, path=["response"])

    @parametrize
    async def test_streaming_response_finetune(self, async_client: AsyncObjective) -> None:
        async with async_client.indexes.with_streaming_response.finetune(
            index_id="idx_123",
            feedback=[{"query": "query"}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            index = await response.parse()
            assert_matches_type(IndexFinetuneResponse, index, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_finetune(self, async_client: AsyncObjective) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `index_id` but received ''"):
            await async_client.indexes.with_raw_response.finetune(
                index_id="",
                feedback=[{"query": "query"}],
            )

    @parametrize
    async def test_method_get(self, async_client: AsyncObjective) -> None:
        index = await async_client.indexes.get(
            "idx_1234",
        )
        assert_matches_type(IndexGetResponse, index, path=["response"])

    @parametrize
    async def test_raw_response_get(self, async_client: AsyncObjective) -> None:
        response = await async_client.indexes.with_raw_response.get(
            "idx_1234",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        index = await response.parse()
        assert_matches_type(IndexGetResponse, index, path=["response"])

    @parametrize
    async def test_streaming_response_get(self, async_client: AsyncObjective) -> None:
        async with async_client.indexes.with_streaming_response.get(
            "idx_1234",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            index = await response.parse()
            assert_matches_type(IndexGetResponse, index, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_get(self, async_client: AsyncObjective) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `index_id` but received ''"):
            await async_client.indexes.with_raw_response.get(
                "",
            )

    @parametrize
    async def test_method_search(self, async_client: AsyncObjective) -> None:
        index = await async_client.indexes.search(
            index_id="idx_123",
        )
        assert_matches_type(IndexSearchResponse, index, path=["response"])

    @parametrize
    async def test_method_search_with_all_params(self, async_client: AsyncObjective) -> None:
        index = await async_client.indexes.search(
            index_id="idx_123",
            filter_query="filter_query",
            limit=0,
            object_fields="object_fields",
            offset=0,
            query="query",
            ranking_expr="ranking_expr",
            relevance_cutoff="relevance_cutoff",
            result_fields="result_fields",
        )
        assert_matches_type(IndexSearchResponse, index, path=["response"])

    @parametrize
    async def test_raw_response_search(self, async_client: AsyncObjective) -> None:
        response = await async_client.indexes.with_raw_response.search(
            index_id="idx_123",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        index = await response.parse()
        assert_matches_type(IndexSearchResponse, index, path=["response"])

    @parametrize
    async def test_streaming_response_search(self, async_client: AsyncObjective) -> None:
        async with async_client.indexes.with_streaming_response.search(
            index_id="idx_123",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            index = await response.parse()
            assert_matches_type(IndexSearchResponse, index, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_search(self, async_client: AsyncObjective) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `index_id` but received ''"):
            await async_client.indexes.with_raw_response.search(
                index_id="",
            )

    @parametrize
    async def test_method_status(self, async_client: AsyncObjective) -> None:
        index = await async_client.indexes.status(
            "idx_1234",
        )
        assert_matches_type(IndexStatusResponse, index, path=["response"])

    @parametrize
    async def test_raw_response_status(self, async_client: AsyncObjective) -> None:
        response = await async_client.indexes.with_raw_response.status(
            "idx_1234",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        index = await response.parse()
        assert_matches_type(IndexStatusResponse, index, path=["response"])

    @parametrize
    async def test_streaming_response_status(self, async_client: AsyncObjective) -> None:
        async with async_client.indexes.with_streaming_response.status(
            "idx_1234",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            index = await response.parse()
            assert_matches_type(IndexStatusResponse, index, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_status(self, async_client: AsyncObjective) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `index_id` but received ''"):
            await async_client.indexes.with_raw_response.status(
                "",
            )

    @parametrize
    async def test_method_status_by_type(self, async_client: AsyncObjective) -> None:
        index = await async_client.indexes.status_by_type(
            index_status_type="UPLOADED",
            index_id="idx_123",
        )
        assert_matches_type(IndexStatusByTypeResponse, index, path=["response"])

    @parametrize
    async def test_raw_response_status_by_type(self, async_client: AsyncObjective) -> None:
        response = await async_client.indexes.with_raw_response.status_by_type(
            index_status_type="UPLOADED",
            index_id="idx_123",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        index = await response.parse()
        assert_matches_type(IndexStatusByTypeResponse, index, path=["response"])

    @parametrize
    async def test_streaming_response_status_by_type(self, async_client: AsyncObjective) -> None:
        async with async_client.indexes.with_streaming_response.status_by_type(
            index_status_type="UPLOADED",
            index_id="idx_123",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            index = await response.parse()
            assert_matches_type(IndexStatusByTypeResponse, index, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_status_by_type(self, async_client: AsyncObjective) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `index_id` but received ''"):
            await async_client.indexes.with_raw_response.status_by_type(
                index_status_type="UPLOADED",
                index_id="",
            )
