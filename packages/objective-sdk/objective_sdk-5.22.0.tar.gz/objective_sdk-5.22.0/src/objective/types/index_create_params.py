# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable
from typing_extensions import Literal, Required, TypedDict

__all__ = [
    "IndexCreateParams",
    "Configuration",
    "ConfigurationFields",
    "ConfigurationFieldsSearchable",
    "ConfigurationFieldsCrawlable",
    "ConfigurationFieldsFilterable",
    "ConfigurationIndexType",
    "ConfigurationIndexTypeFinetuning",
    "ConfigurationIndexTypeFinetuningFeedback",
    "ConfigurationIndexTypeHighlights",
]


class IndexCreateParams(TypedDict, total=False):
    configuration: Required[Configuration]


class ConfigurationFieldsSearchable(TypedDict, total=False):
    allow: Required[List[str]]


class ConfigurationFieldsCrawlable(TypedDict, total=False):
    allow: List[str]


class ConfigurationFieldsFilterable(TypedDict, total=False):
    allow: List[str]


class ConfigurationFields(TypedDict, total=False):
    searchable: Required[ConfigurationFieldsSearchable]

    crawlable: ConfigurationFieldsCrawlable

    fast_filters: List[str]

    filterable: ConfigurationFieldsFilterable

    segment_delimiter: Dict[str, object]

    types: Dict[str, str]


class ConfigurationIndexTypeFinetuningFeedback(TypedDict, total=False):
    query: Required[str]

    label: Literal["GREAT", "OK", "BAD"]

    object_id: str


class ConfigurationIndexTypeFinetuning(TypedDict, total=False):
    base_index_id: Required[str]

    feedback: Required[Iterable[ConfigurationIndexTypeFinetuningFeedback]]


class ConfigurationIndexTypeHighlights(TypedDict, total=False):
    text: bool


class ConfigurationIndexType(TypedDict, total=False):
    name: Required[Union[Literal["multimodal", "text", "image", "multimodal-neural", "text-neural"], str]]

    finetuning: ConfigurationIndexTypeFinetuning

    highlights: ConfigurationIndexTypeHighlights

    version: str


class Configuration(TypedDict, total=False):
    fields: Required[ConfigurationFields]

    index_type: ConfigurationIndexType
