"""
Main interface for forecastquery service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_forecastquery import (
        Client,
        ForecastQueryServiceClient,
    )

    session = Session()
    client: ForecastQueryServiceClient = session.client("forecastquery")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import ForecastQueryServiceClient

Client = ForecastQueryServiceClient


__all__ = ("Client", "ForecastQueryServiceClient")
