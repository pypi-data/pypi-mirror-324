"""
Main interface for securitylake service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_securitylake import (
        Client,
        GetDataLakeSourcesPaginator,
        ListDataLakeExceptionsPaginator,
        ListLogSourcesPaginator,
        ListSubscribersPaginator,
        SecurityLakeClient,
    )

    session = Session()
    client: SecurityLakeClient = session.client("securitylake")

    get_data_lake_sources_paginator: GetDataLakeSourcesPaginator = client.get_paginator("get_data_lake_sources")
    list_data_lake_exceptions_paginator: ListDataLakeExceptionsPaginator = client.get_paginator("list_data_lake_exceptions")
    list_log_sources_paginator: ListLogSourcesPaginator = client.get_paginator("list_log_sources")
    list_subscribers_paginator: ListSubscribersPaginator = client.get_paginator("list_subscribers")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import SecurityLakeClient
from .paginator import (
    GetDataLakeSourcesPaginator,
    ListDataLakeExceptionsPaginator,
    ListLogSourcesPaginator,
    ListSubscribersPaginator,
)

Client = SecurityLakeClient

__all__ = (
    "Client",
    "GetDataLakeSourcesPaginator",
    "ListDataLakeExceptionsPaginator",
    "ListLogSourcesPaginator",
    "ListSubscribersPaginator",
    "SecurityLakeClient",
)
