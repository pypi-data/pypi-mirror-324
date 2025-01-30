"""
Main interface for braket service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_braket import (
        BraketClient,
        Client,
        SearchDevicesPaginator,
        SearchJobsPaginator,
        SearchQuantumTasksPaginator,
    )

    session = Session()
    client: BraketClient = session.client("braket")

    search_devices_paginator: SearchDevicesPaginator = client.get_paginator("search_devices")
    search_jobs_paginator: SearchJobsPaginator = client.get_paginator("search_jobs")
    search_quantum_tasks_paginator: SearchQuantumTasksPaginator = client.get_paginator("search_quantum_tasks")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import BraketClient
from .paginator import SearchDevicesPaginator, SearchJobsPaginator, SearchQuantumTasksPaginator

Client = BraketClient

__all__ = (
    "BraketClient",
    "Client",
    "SearchDevicesPaginator",
    "SearchJobsPaginator",
    "SearchQuantumTasksPaginator",
)
