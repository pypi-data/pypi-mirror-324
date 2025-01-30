"""
Main interface for invoicing service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_invoicing import (
        Client,
        InvoicingClient,
        ListInvoiceUnitsPaginator,
    )

    session = Session()
    client: InvoicingClient = session.client("invoicing")

    list_invoice_units_paginator: ListInvoiceUnitsPaginator = client.get_paginator("list_invoice_units")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import InvoicingClient
from .paginator import ListInvoiceUnitsPaginator

Client = InvoicingClient


__all__ = ("Client", "InvoicingClient", "ListInvoiceUnitsPaginator")
