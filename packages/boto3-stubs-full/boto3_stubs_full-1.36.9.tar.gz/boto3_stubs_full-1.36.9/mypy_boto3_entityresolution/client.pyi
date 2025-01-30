"""
Type annotations for entityresolution service Client.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_entityresolution.client import EntityResolutionClient

    session = Session()
    client: EntityResolutionClient = session.client("entityresolution")
    ```

Copyright 2025 Vlad Emelianov
"""

from __future__ import annotations

import sys
from typing import Any, overload

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    ListIdMappingJobsPaginator,
    ListIdMappingWorkflowsPaginator,
    ListIdNamespacesPaginator,
    ListMatchingJobsPaginator,
    ListMatchingWorkflowsPaginator,
    ListProviderServicesPaginator,
    ListSchemaMappingsPaginator,
)
from .type_defs import (
    AddPolicyStatementInputRequestTypeDef,
    AddPolicyStatementOutputTypeDef,
    BatchDeleteUniqueIdInputRequestTypeDef,
    BatchDeleteUniqueIdOutputTypeDef,
    CreateIdMappingWorkflowInputRequestTypeDef,
    CreateIdMappingWorkflowOutputTypeDef,
    CreateIdNamespaceInputRequestTypeDef,
    CreateIdNamespaceOutputTypeDef,
    CreateMatchingWorkflowInputRequestTypeDef,
    CreateMatchingWorkflowOutputTypeDef,
    CreateSchemaMappingInputRequestTypeDef,
    CreateSchemaMappingOutputTypeDef,
    DeleteIdMappingWorkflowInputRequestTypeDef,
    DeleteIdMappingWorkflowOutputTypeDef,
    DeleteIdNamespaceInputRequestTypeDef,
    DeleteIdNamespaceOutputTypeDef,
    DeleteMatchingWorkflowInputRequestTypeDef,
    DeleteMatchingWorkflowOutputTypeDef,
    DeletePolicyStatementInputRequestTypeDef,
    DeletePolicyStatementOutputTypeDef,
    DeleteSchemaMappingInputRequestTypeDef,
    DeleteSchemaMappingOutputTypeDef,
    GetIdMappingJobInputRequestTypeDef,
    GetIdMappingJobOutputTypeDef,
    GetIdMappingWorkflowInputRequestTypeDef,
    GetIdMappingWorkflowOutputTypeDef,
    GetIdNamespaceInputRequestTypeDef,
    GetIdNamespaceOutputTypeDef,
    GetMatchIdInputRequestTypeDef,
    GetMatchIdOutputTypeDef,
    GetMatchingJobInputRequestTypeDef,
    GetMatchingJobOutputTypeDef,
    GetMatchingWorkflowInputRequestTypeDef,
    GetMatchingWorkflowOutputTypeDef,
    GetPolicyInputRequestTypeDef,
    GetPolicyOutputTypeDef,
    GetProviderServiceInputRequestTypeDef,
    GetProviderServiceOutputTypeDef,
    GetSchemaMappingInputRequestTypeDef,
    GetSchemaMappingOutputTypeDef,
    ListIdMappingJobsInputRequestTypeDef,
    ListIdMappingJobsOutputTypeDef,
    ListIdMappingWorkflowsInputRequestTypeDef,
    ListIdMappingWorkflowsOutputTypeDef,
    ListIdNamespacesInputRequestTypeDef,
    ListIdNamespacesOutputTypeDef,
    ListMatchingJobsInputRequestTypeDef,
    ListMatchingJobsOutputTypeDef,
    ListMatchingWorkflowsInputRequestTypeDef,
    ListMatchingWorkflowsOutputTypeDef,
    ListProviderServicesInputRequestTypeDef,
    ListProviderServicesOutputTypeDef,
    ListSchemaMappingsInputRequestTypeDef,
    ListSchemaMappingsOutputTypeDef,
    ListTagsForResourceInputRequestTypeDef,
    ListTagsForResourceOutputTypeDef,
    PutPolicyInputRequestTypeDef,
    PutPolicyOutputTypeDef,
    StartIdMappingJobInputRequestTypeDef,
    StartIdMappingJobOutputTypeDef,
    StartMatchingJobInputRequestTypeDef,
    StartMatchingJobOutputTypeDef,
    TagResourceInputRequestTypeDef,
    UntagResourceInputRequestTypeDef,
    UpdateIdMappingWorkflowInputRequestTypeDef,
    UpdateIdMappingWorkflowOutputTypeDef,
    UpdateIdNamespaceInputRequestTypeDef,
    UpdateIdNamespaceOutputTypeDef,
    UpdateMatchingWorkflowInputRequestTypeDef,
    UpdateMatchingWorkflowOutputTypeDef,
    UpdateSchemaMappingInputRequestTypeDef,
    UpdateSchemaMappingOutputTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("EntityResolutionClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ExceedsLimitException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class EntityResolutionClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        EntityResolutionClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#generate_presigned_url)
        """

    def add_policy_statement(
        self, **kwargs: Unpack[AddPolicyStatementInputRequestTypeDef]
    ) -> AddPolicyStatementOutputTypeDef:
        """
        Adds a policy statement object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/add_policy_statement.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#add_policy_statement)
        """

    def batch_delete_unique_id(
        self, **kwargs: Unpack[BatchDeleteUniqueIdInputRequestTypeDef]
    ) -> BatchDeleteUniqueIdOutputTypeDef:
        """
        Deletes multiple unique IDs in a matching workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/batch_delete_unique_id.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#batch_delete_unique_id)
        """

    def create_id_mapping_workflow(
        self, **kwargs: Unpack[CreateIdMappingWorkflowInputRequestTypeDef]
    ) -> CreateIdMappingWorkflowOutputTypeDef:
        """
        Creates an <code>IdMappingWorkflow</code> object which stores the configuration
        of the data processing job to be run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/create_id_mapping_workflow.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#create_id_mapping_workflow)
        """

    def create_id_namespace(
        self, **kwargs: Unpack[CreateIdNamespaceInputRequestTypeDef]
    ) -> CreateIdNamespaceOutputTypeDef:
        """
        Creates an ID namespace object which will help customers provide metadata
        explaining their dataset and how to use it.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/create_id_namespace.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#create_id_namespace)
        """

    def create_matching_workflow(
        self, **kwargs: Unpack[CreateMatchingWorkflowInputRequestTypeDef]
    ) -> CreateMatchingWorkflowOutputTypeDef:
        """
        Creates a <code>MatchingWorkflow</code> object which stores the configuration
        of the data processing job to be run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/create_matching_workflow.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#create_matching_workflow)
        """

    def create_schema_mapping(
        self, **kwargs: Unpack[CreateSchemaMappingInputRequestTypeDef]
    ) -> CreateSchemaMappingOutputTypeDef:
        """
        Creates a schema mapping, which defines the schema of the input customer
        records table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/create_schema_mapping.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#create_schema_mapping)
        """

    def delete_id_mapping_workflow(
        self, **kwargs: Unpack[DeleteIdMappingWorkflowInputRequestTypeDef]
    ) -> DeleteIdMappingWorkflowOutputTypeDef:
        """
        Deletes the <code>IdMappingWorkflow</code> with a given name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/delete_id_mapping_workflow.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#delete_id_mapping_workflow)
        """

    def delete_id_namespace(
        self, **kwargs: Unpack[DeleteIdNamespaceInputRequestTypeDef]
    ) -> DeleteIdNamespaceOutputTypeDef:
        """
        Deletes the <code>IdNamespace</code> with a given name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/delete_id_namespace.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#delete_id_namespace)
        """

    def delete_matching_workflow(
        self, **kwargs: Unpack[DeleteMatchingWorkflowInputRequestTypeDef]
    ) -> DeleteMatchingWorkflowOutputTypeDef:
        """
        Deletes the <code>MatchingWorkflow</code> with a given name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/delete_matching_workflow.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#delete_matching_workflow)
        """

    def delete_policy_statement(
        self, **kwargs: Unpack[DeletePolicyStatementInputRequestTypeDef]
    ) -> DeletePolicyStatementOutputTypeDef:
        """
        Deletes the policy statement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/delete_policy_statement.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#delete_policy_statement)
        """

    def delete_schema_mapping(
        self, **kwargs: Unpack[DeleteSchemaMappingInputRequestTypeDef]
    ) -> DeleteSchemaMappingOutputTypeDef:
        """
        Deletes the <code>SchemaMapping</code> with a given name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/delete_schema_mapping.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#delete_schema_mapping)
        """

    def get_id_mapping_job(
        self, **kwargs: Unpack[GetIdMappingJobInputRequestTypeDef]
    ) -> GetIdMappingJobOutputTypeDef:
        """
        Gets the status, metrics, and errors (if there are any) that are associated
        with a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/get_id_mapping_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#get_id_mapping_job)
        """

    def get_id_mapping_workflow(
        self, **kwargs: Unpack[GetIdMappingWorkflowInputRequestTypeDef]
    ) -> GetIdMappingWorkflowOutputTypeDef:
        """
        Returns the <code>IdMappingWorkflow</code> with a given name, if it exists.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/get_id_mapping_workflow.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#get_id_mapping_workflow)
        """

    def get_id_namespace(
        self, **kwargs: Unpack[GetIdNamespaceInputRequestTypeDef]
    ) -> GetIdNamespaceOutputTypeDef:
        """
        Returns the <code>IdNamespace</code> with a given name, if it exists.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/get_id_namespace.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#get_id_namespace)
        """

    def get_match_id(
        self, **kwargs: Unpack[GetMatchIdInputRequestTypeDef]
    ) -> GetMatchIdOutputTypeDef:
        """
        Returns the corresponding Match ID of a customer record if the record has been
        processed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/get_match_id.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#get_match_id)
        """

    def get_matching_job(
        self, **kwargs: Unpack[GetMatchingJobInputRequestTypeDef]
    ) -> GetMatchingJobOutputTypeDef:
        """
        Gets the status, metrics, and errors (if there are any) that are associated
        with a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/get_matching_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#get_matching_job)
        """

    def get_matching_workflow(
        self, **kwargs: Unpack[GetMatchingWorkflowInputRequestTypeDef]
    ) -> GetMatchingWorkflowOutputTypeDef:
        """
        Returns the <code>MatchingWorkflow</code> with a given name, if it exists.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/get_matching_workflow.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#get_matching_workflow)
        """

    def get_policy(self, **kwargs: Unpack[GetPolicyInputRequestTypeDef]) -> GetPolicyOutputTypeDef:
        """
        Returns the resource-based policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/get_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#get_policy)
        """

    def get_provider_service(
        self, **kwargs: Unpack[GetProviderServiceInputRequestTypeDef]
    ) -> GetProviderServiceOutputTypeDef:
        """
        Returns the <code>ProviderService</code> of a given name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/get_provider_service.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#get_provider_service)
        """

    def get_schema_mapping(
        self, **kwargs: Unpack[GetSchemaMappingInputRequestTypeDef]
    ) -> GetSchemaMappingOutputTypeDef:
        """
        Returns the SchemaMapping of a given name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/get_schema_mapping.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#get_schema_mapping)
        """

    def list_id_mapping_jobs(
        self, **kwargs: Unpack[ListIdMappingJobsInputRequestTypeDef]
    ) -> ListIdMappingJobsOutputTypeDef:
        """
        Lists all ID mapping jobs for a given workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/list_id_mapping_jobs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#list_id_mapping_jobs)
        """

    def list_id_mapping_workflows(
        self, **kwargs: Unpack[ListIdMappingWorkflowsInputRequestTypeDef]
    ) -> ListIdMappingWorkflowsOutputTypeDef:
        """
        Returns a list of all the <code>IdMappingWorkflows</code> that have been
        created for an Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/list_id_mapping_workflows.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#list_id_mapping_workflows)
        """

    def list_id_namespaces(
        self, **kwargs: Unpack[ListIdNamespacesInputRequestTypeDef]
    ) -> ListIdNamespacesOutputTypeDef:
        """
        Returns a list of all ID namespaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/list_id_namespaces.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#list_id_namespaces)
        """

    def list_matching_jobs(
        self, **kwargs: Unpack[ListMatchingJobsInputRequestTypeDef]
    ) -> ListMatchingJobsOutputTypeDef:
        """
        Lists all jobs for a given workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/list_matching_jobs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#list_matching_jobs)
        """

    def list_matching_workflows(
        self, **kwargs: Unpack[ListMatchingWorkflowsInputRequestTypeDef]
    ) -> ListMatchingWorkflowsOutputTypeDef:
        """
        Returns a list of all the <code>MatchingWorkflows</code> that have been created
        for an Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/list_matching_workflows.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#list_matching_workflows)
        """

    def list_provider_services(
        self, **kwargs: Unpack[ListProviderServicesInputRequestTypeDef]
    ) -> ListProviderServicesOutputTypeDef:
        """
        Returns a list of all the <code>ProviderServices</code> that are available in
        this Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/list_provider_services.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#list_provider_services)
        """

    def list_schema_mappings(
        self, **kwargs: Unpack[ListSchemaMappingsInputRequestTypeDef]
    ) -> ListSchemaMappingsOutputTypeDef:
        """
        Returns a list of all the <code>SchemaMappings</code> that have been created
        for an Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/list_schema_mappings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#list_schema_mappings)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputRequestTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Displays the tags associated with an Entity Resolution resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#list_tags_for_resource)
        """

    def put_policy(self, **kwargs: Unpack[PutPolicyInputRequestTypeDef]) -> PutPolicyOutputTypeDef:
        """
        Updates the resource-based policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/put_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#put_policy)
        """

    def start_id_mapping_job(
        self, **kwargs: Unpack[StartIdMappingJobInputRequestTypeDef]
    ) -> StartIdMappingJobOutputTypeDef:
        """
        Starts the <code>IdMappingJob</code> of a workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/start_id_mapping_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#start_id_mapping_job)
        """

    def start_matching_job(
        self, **kwargs: Unpack[StartMatchingJobInputRequestTypeDef]
    ) -> StartMatchingJobOutputTypeDef:
        """
        Starts the <code>MatchingJob</code> of a workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/start_matching_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#start_matching_job)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Assigns one or more tags (key-value pairs) to the specified Entity Resolution
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#tag_resource)
        """

    def untag_resource(self, **kwargs: Unpack[UntagResourceInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes one or more tags from the specified Entity Resolution resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#untag_resource)
        """

    def update_id_mapping_workflow(
        self, **kwargs: Unpack[UpdateIdMappingWorkflowInputRequestTypeDef]
    ) -> UpdateIdMappingWorkflowOutputTypeDef:
        """
        Updates an existing <code>IdMappingWorkflow</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/update_id_mapping_workflow.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#update_id_mapping_workflow)
        """

    def update_id_namespace(
        self, **kwargs: Unpack[UpdateIdNamespaceInputRequestTypeDef]
    ) -> UpdateIdNamespaceOutputTypeDef:
        """
        Updates an existing ID namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/update_id_namespace.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#update_id_namespace)
        """

    def update_matching_workflow(
        self, **kwargs: Unpack[UpdateMatchingWorkflowInputRequestTypeDef]
    ) -> UpdateMatchingWorkflowOutputTypeDef:
        """
        Updates an existing <code>MatchingWorkflow</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/update_matching_workflow.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#update_matching_workflow)
        """

    def update_schema_mapping(
        self, **kwargs: Unpack[UpdateSchemaMappingInputRequestTypeDef]
    ) -> UpdateSchemaMappingOutputTypeDef:
        """
        Updates a schema mapping.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/update_schema_mapping.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#update_schema_mapping)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_id_mapping_jobs"]
    ) -> ListIdMappingJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_id_mapping_workflows"]
    ) -> ListIdMappingWorkflowsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_id_namespaces"]
    ) -> ListIdNamespacesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_matching_jobs"]
    ) -> ListMatchingJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_matching_workflows"]
    ) -> ListMatchingWorkflowsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_provider_services"]
    ) -> ListProviderServicesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_schema_mappings"]
    ) -> ListSchemaMappingsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#get_paginator)
        """
