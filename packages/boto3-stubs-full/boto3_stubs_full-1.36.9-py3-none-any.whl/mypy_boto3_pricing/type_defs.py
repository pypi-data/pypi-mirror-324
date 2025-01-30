"""
Type annotations for pricing service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pricing/type_defs/)

Usage::

    ```python
    from mypy_boto3_pricing.type_defs import AttributeValueTypeDef

    data: AttributeValueTypeDef = ...
    ```

Copyright 2025 Vlad Emelianov
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import Union

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import list as List
    from collections.abc import Sequence
else:
    from typing import Dict, List, Sequence
if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AttributeValueTypeDef",
    "DescribeServicesRequestPaginateTypeDef",
    "DescribeServicesRequestRequestTypeDef",
    "DescribeServicesResponseTypeDef",
    "FilterTypeDef",
    "GetAttributeValuesRequestPaginateTypeDef",
    "GetAttributeValuesRequestRequestTypeDef",
    "GetAttributeValuesResponseTypeDef",
    "GetPriceListFileUrlRequestRequestTypeDef",
    "GetPriceListFileUrlResponseTypeDef",
    "GetProductsRequestPaginateTypeDef",
    "GetProductsRequestRequestTypeDef",
    "GetProductsResponseTypeDef",
    "ListPriceListsRequestPaginateTypeDef",
    "ListPriceListsRequestRequestTypeDef",
    "ListPriceListsResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PriceListTypeDef",
    "ResponseMetadataTypeDef",
    "ServiceTypeDef",
    "TimestampTypeDef",
)


class AttributeValueTypeDef(TypedDict):
    Value: NotRequired[str]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class DescribeServicesRequestRequestTypeDef(TypedDict):
    ServiceCode: NotRequired[str]
    FormatVersion: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class ServiceTypeDef(TypedDict):
    ServiceCode: str
    AttributeNames: NotRequired[List[str]]


FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "Type": Literal["TERM_MATCH"],
        "Field": str,
        "Value": str,
    },
)


class GetAttributeValuesRequestRequestTypeDef(TypedDict):
    ServiceCode: str
    AttributeName: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class GetPriceListFileUrlRequestRequestTypeDef(TypedDict):
    PriceListArn: str
    FileFormat: str


TimestampTypeDef = Union[datetime, str]


class PriceListTypeDef(TypedDict):
    PriceListArn: NotRequired[str]
    RegionCode: NotRequired[str]
    CurrencyCode: NotRequired[str]
    FileFormats: NotRequired[List[str]]


class DescribeServicesRequestPaginateTypeDef(TypedDict):
    ServiceCode: NotRequired[str]
    FormatVersion: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetAttributeValuesRequestPaginateTypeDef(TypedDict):
    ServiceCode: str
    AttributeName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetAttributeValuesResponseTypeDef(TypedDict):
    AttributeValues: List[AttributeValueTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetPriceListFileUrlResponseTypeDef(TypedDict):
    Url: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetProductsResponseTypeDef(TypedDict):
    FormatVersion: str
    PriceList: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeServicesResponseTypeDef(TypedDict):
    Services: List[ServiceTypeDef]
    FormatVersion: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetProductsRequestPaginateTypeDef(TypedDict):
    ServiceCode: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    FormatVersion: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetProductsRequestRequestTypeDef(TypedDict):
    ServiceCode: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    FormatVersion: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListPriceListsRequestPaginateTypeDef(TypedDict):
    ServiceCode: str
    EffectiveDate: TimestampTypeDef
    CurrencyCode: str
    RegionCode: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPriceListsRequestRequestTypeDef(TypedDict):
    ServiceCode: str
    EffectiveDate: TimestampTypeDef
    CurrencyCode: str
    RegionCode: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListPriceListsResponseTypeDef(TypedDict):
    PriceLists: List[PriceListTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]
