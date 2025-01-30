"""
Main interface for kinesis-video-signaling service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_kinesis_video_signaling import (
        Client,
        KinesisVideoSignalingChannelsClient,
    )

    session = Session()
    client: KinesisVideoSignalingChannelsClient = session.client("kinesis-video-signaling")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import KinesisVideoSignalingChannelsClient

Client = KinesisVideoSignalingChannelsClient


__all__ = ("Client", "KinesisVideoSignalingChannelsClient")
