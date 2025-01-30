"""
Main interface for serverlessrepo service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_serverlessrepo import (
        Client,
        ListApplicationDependenciesPaginator,
        ListApplicationVersionsPaginator,
        ListApplicationsPaginator,
        ServerlessApplicationRepositoryClient,
    )

    session = Session()
    client: ServerlessApplicationRepositoryClient = session.client("serverlessrepo")

    list_application_dependencies_paginator: ListApplicationDependenciesPaginator = client.get_paginator("list_application_dependencies")
    list_application_versions_paginator: ListApplicationVersionsPaginator = client.get_paginator("list_application_versions")
    list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import ServerlessApplicationRepositoryClient
from .paginator import (
    ListApplicationDependenciesPaginator,
    ListApplicationsPaginator,
    ListApplicationVersionsPaginator,
)

Client = ServerlessApplicationRepositoryClient

__all__ = (
    "Client",
    "ListApplicationDependenciesPaginator",
    "ListApplicationVersionsPaginator",
    "ListApplicationsPaginator",
    "ServerlessApplicationRepositoryClient",
)
