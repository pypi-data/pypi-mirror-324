"""
Type annotations for workmailmessageflow service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workmailmessageflow/type_defs/)

Usage::

    ```python
    from mypy_boto3_workmailmessageflow.type_defs import GetRawMessageContentRequestRequestTypeDef

    data: GetRawMessageContentRequestRequestTypeDef = ...
    ```

Copyright 2025 Vlad Emelianov
"""

from __future__ import annotations

import sys

from botocore.response import StreamingBody

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
else:
    from typing import Dict
if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "GetRawMessageContentRequestRequestTypeDef",
    "GetRawMessageContentResponseTypeDef",
    "PutRawMessageContentRequestRequestTypeDef",
    "RawMessageContentTypeDef",
    "ResponseMetadataTypeDef",
    "S3ReferenceTypeDef",
)

class GetRawMessageContentRequestRequestTypeDef(TypedDict):
    messageId: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class S3ReferenceTypeDef(TypedDict):
    bucket: str
    key: str
    objectVersion: NotRequired[str]

class GetRawMessageContentResponseTypeDef(TypedDict):
    messageContent: StreamingBody
    ResponseMetadata: ResponseMetadataTypeDef

class RawMessageContentTypeDef(TypedDict):
    s3Reference: S3ReferenceTypeDef

class PutRawMessageContentRequestRequestTypeDef(TypedDict):
    messageId: str
    content: RawMessageContentTypeDef
