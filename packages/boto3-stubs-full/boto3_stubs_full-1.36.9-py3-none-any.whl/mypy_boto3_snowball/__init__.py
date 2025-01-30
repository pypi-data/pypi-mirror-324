"""
Main interface for snowball service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_snowball import (
        Client,
        DescribeAddressesPaginator,
        ListClusterJobsPaginator,
        ListClustersPaginator,
        ListCompatibleImagesPaginator,
        ListJobsPaginator,
        ListLongTermPricingPaginator,
        SnowballClient,
    )

    session = Session()
    client: SnowballClient = session.client("snowball")

    describe_addresses_paginator: DescribeAddressesPaginator = client.get_paginator("describe_addresses")
    list_cluster_jobs_paginator: ListClusterJobsPaginator = client.get_paginator("list_cluster_jobs")
    list_clusters_paginator: ListClustersPaginator = client.get_paginator("list_clusters")
    list_compatible_images_paginator: ListCompatibleImagesPaginator = client.get_paginator("list_compatible_images")
    list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
    list_long_term_pricing_paginator: ListLongTermPricingPaginator = client.get_paginator("list_long_term_pricing")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import SnowballClient
from .paginator import (
    DescribeAddressesPaginator,
    ListClusterJobsPaginator,
    ListClustersPaginator,
    ListCompatibleImagesPaginator,
    ListJobsPaginator,
    ListLongTermPricingPaginator,
)

Client = SnowballClient


__all__ = (
    "Client",
    "DescribeAddressesPaginator",
    "ListClusterJobsPaginator",
    "ListClustersPaginator",
    "ListCompatibleImagesPaginator",
    "ListJobsPaginator",
    "ListLongTermPricingPaginator",
    "SnowballClient",
)
