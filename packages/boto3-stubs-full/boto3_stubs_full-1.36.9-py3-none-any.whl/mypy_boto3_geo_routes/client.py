"""
Type annotations for geo-routes service Client.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_routes/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_geo_routes.client import LocationServiceRoutesV2Client

    session = Session()
    client: LocationServiceRoutesV2Client = session.client("geo-routes")
    ```

Copyright 2025 Vlad Emelianov
"""

from __future__ import annotations

import sys
from typing import Any

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .type_defs import (
    CalculateIsolinesRequestRequestTypeDef,
    CalculateIsolinesResponseTypeDef,
    CalculateRouteMatrixRequestRequestTypeDef,
    CalculateRouteMatrixResponseTypeDef,
    CalculateRoutesRequestRequestTypeDef,
    CalculateRoutesResponseTypeDef,
    OptimizeWaypointsRequestRequestTypeDef,
    OptimizeWaypointsResponseTypeDef,
    SnapToRoadsRequestRequestTypeDef,
    SnapToRoadsResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("LocationServiceRoutesV2Client",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class LocationServiceRoutesV2Client(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-routes.html#LocationServiceRoutesV2.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_routes/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        LocationServiceRoutesV2Client exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-routes.html#LocationServiceRoutesV2.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_routes/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-routes/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_routes/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-routes/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_routes/client/#generate_presigned_url)
        """

    def calculate_isolines(
        self, **kwargs: Unpack[CalculateIsolinesRequestRequestTypeDef]
    ) -> CalculateIsolinesResponseTypeDef:
        """
        Use the <code>CalculateIsolines</code> action to find service areas that can be
        reached in a given threshold of time, distance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-routes/client/calculate_isolines.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_routes/client/#calculate_isolines)
        """

    def calculate_route_matrix(
        self, **kwargs: Unpack[CalculateRouteMatrixRequestRequestTypeDef]
    ) -> CalculateRouteMatrixResponseTypeDef:
        """
        Calculates route matrix containing the results for all pairs of Origins to
        Destinations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-routes/client/calculate_route_matrix.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_routes/client/#calculate_route_matrix)
        """

    def calculate_routes(
        self, **kwargs: Unpack[CalculateRoutesRequestRequestTypeDef]
    ) -> CalculateRoutesResponseTypeDef:
        """
        Calculates a route given the following required parameters: <code>Origin</code>
        and <code>Destination</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-routes/client/calculate_routes.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_routes/client/#calculate_routes)
        """

    def optimize_waypoints(
        self, **kwargs: Unpack[OptimizeWaypointsRequestRequestTypeDef]
    ) -> OptimizeWaypointsResponseTypeDef:
        """
        Calculates the optimal order to travel between a set of waypoints to minimize
        either the travel time or the distance travelled during the journey, based on
        road network restrictions and the traffic pattern data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-routes/client/optimize_waypoints.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_routes/client/#optimize_waypoints)
        """

    def snap_to_roads(
        self, **kwargs: Unpack[SnapToRoadsRequestRequestTypeDef]
    ) -> SnapToRoadsResponseTypeDef:
        """
        The SnapToRoads action matches GPS trace to roads most likely traveled on.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-routes/client/snap_to_roads.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_routes/client/#snap_to_roads)
        """
