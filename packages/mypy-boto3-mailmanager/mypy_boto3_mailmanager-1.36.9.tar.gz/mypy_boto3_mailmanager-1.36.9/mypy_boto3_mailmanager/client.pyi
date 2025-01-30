"""
Type annotations for mailmanager service Client.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_mailmanager.client import MailManagerClient

    session = Session()
    client: MailManagerClient = session.client("mailmanager")
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
    ListAddonInstancesPaginator,
    ListAddonSubscriptionsPaginator,
    ListAddressListImportJobsPaginator,
    ListAddressListsPaginator,
    ListArchiveExportsPaginator,
    ListArchiveSearchesPaginator,
    ListArchivesPaginator,
    ListIngressPointsPaginator,
    ListMembersOfAddressListPaginator,
    ListRelaysPaginator,
    ListRuleSetsPaginator,
    ListTrafficPoliciesPaginator,
)
from .type_defs import (
    CreateAddonInstanceRequestRequestTypeDef,
    CreateAddonInstanceResponseTypeDef,
    CreateAddonSubscriptionRequestRequestTypeDef,
    CreateAddonSubscriptionResponseTypeDef,
    CreateAddressListImportJobRequestRequestTypeDef,
    CreateAddressListImportJobResponseTypeDef,
    CreateAddressListRequestRequestTypeDef,
    CreateAddressListResponseTypeDef,
    CreateArchiveRequestRequestTypeDef,
    CreateArchiveResponseTypeDef,
    CreateIngressPointRequestRequestTypeDef,
    CreateIngressPointResponseTypeDef,
    CreateRelayRequestRequestTypeDef,
    CreateRelayResponseTypeDef,
    CreateRuleSetRequestRequestTypeDef,
    CreateRuleSetResponseTypeDef,
    CreateTrafficPolicyRequestRequestTypeDef,
    CreateTrafficPolicyResponseTypeDef,
    DeleteAddonInstanceRequestRequestTypeDef,
    DeleteAddonSubscriptionRequestRequestTypeDef,
    DeleteAddressListRequestRequestTypeDef,
    DeleteArchiveRequestRequestTypeDef,
    DeleteIngressPointRequestRequestTypeDef,
    DeleteRelayRequestRequestTypeDef,
    DeleteRuleSetRequestRequestTypeDef,
    DeleteTrafficPolicyRequestRequestTypeDef,
    DeregisterMemberFromAddressListRequestRequestTypeDef,
    GetAddonInstanceRequestRequestTypeDef,
    GetAddonInstanceResponseTypeDef,
    GetAddonSubscriptionRequestRequestTypeDef,
    GetAddonSubscriptionResponseTypeDef,
    GetAddressListImportJobRequestRequestTypeDef,
    GetAddressListImportJobResponseTypeDef,
    GetAddressListRequestRequestTypeDef,
    GetAddressListResponseTypeDef,
    GetArchiveExportRequestRequestTypeDef,
    GetArchiveExportResponseTypeDef,
    GetArchiveMessageContentRequestRequestTypeDef,
    GetArchiveMessageContentResponseTypeDef,
    GetArchiveMessageRequestRequestTypeDef,
    GetArchiveMessageResponseTypeDef,
    GetArchiveRequestRequestTypeDef,
    GetArchiveResponseTypeDef,
    GetArchiveSearchRequestRequestTypeDef,
    GetArchiveSearchResponseTypeDef,
    GetArchiveSearchResultsRequestRequestTypeDef,
    GetArchiveSearchResultsResponseTypeDef,
    GetIngressPointRequestRequestTypeDef,
    GetIngressPointResponseTypeDef,
    GetMemberOfAddressListRequestRequestTypeDef,
    GetMemberOfAddressListResponseTypeDef,
    GetRelayRequestRequestTypeDef,
    GetRelayResponseTypeDef,
    GetRuleSetRequestRequestTypeDef,
    GetRuleSetResponseTypeDef,
    GetTrafficPolicyRequestRequestTypeDef,
    GetTrafficPolicyResponseTypeDef,
    ListAddonInstancesRequestRequestTypeDef,
    ListAddonInstancesResponseTypeDef,
    ListAddonSubscriptionsRequestRequestTypeDef,
    ListAddonSubscriptionsResponseTypeDef,
    ListAddressListImportJobsRequestRequestTypeDef,
    ListAddressListImportJobsResponseTypeDef,
    ListAddressListsRequestRequestTypeDef,
    ListAddressListsResponseTypeDef,
    ListArchiveExportsRequestRequestTypeDef,
    ListArchiveExportsResponseTypeDef,
    ListArchiveSearchesRequestRequestTypeDef,
    ListArchiveSearchesResponseTypeDef,
    ListArchivesRequestRequestTypeDef,
    ListArchivesResponseTypeDef,
    ListIngressPointsRequestRequestTypeDef,
    ListIngressPointsResponseTypeDef,
    ListMembersOfAddressListRequestRequestTypeDef,
    ListMembersOfAddressListResponseTypeDef,
    ListRelaysRequestRequestTypeDef,
    ListRelaysResponseTypeDef,
    ListRuleSetsRequestRequestTypeDef,
    ListRuleSetsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTrafficPoliciesRequestRequestTypeDef,
    ListTrafficPoliciesResponseTypeDef,
    RegisterMemberToAddressListRequestRequestTypeDef,
    StartAddressListImportJobRequestRequestTypeDef,
    StartArchiveExportRequestRequestTypeDef,
    StartArchiveExportResponseTypeDef,
    StartArchiveSearchRequestRequestTypeDef,
    StartArchiveSearchResponseTypeDef,
    StopAddressListImportJobRequestRequestTypeDef,
    StopArchiveExportRequestRequestTypeDef,
    StopArchiveSearchRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateArchiveRequestRequestTypeDef,
    UpdateIngressPointRequestRequestTypeDef,
    UpdateRelayRequestRequestTypeDef,
    UpdateRuleSetRequestRequestTypeDef,
    UpdateTrafficPolicyRequestRequestTypeDef,
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

__all__ = ("MailManagerClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class MailManagerClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager.html#MailManager.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MailManagerClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager.html#MailManager.Client)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/can_paginate.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/generate_presigned_url.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#generate_presigned_url)
        """

    def create_addon_instance(
        self, **kwargs: Unpack[CreateAddonInstanceRequestRequestTypeDef]
    ) -> CreateAddonInstanceResponseTypeDef:
        """
        Creates an Add On instance for the subscription indicated in the request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/create_addon_instance.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#create_addon_instance)
        """

    def create_addon_subscription(
        self, **kwargs: Unpack[CreateAddonSubscriptionRequestRequestTypeDef]
    ) -> CreateAddonSubscriptionResponseTypeDef:
        """
        Creates a subscription for an Add On representing the acceptance of its terms
        of use and additional pricing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/create_addon_subscription.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#create_addon_subscription)
        """

    def create_address_list(
        self, **kwargs: Unpack[CreateAddressListRequestRequestTypeDef]
    ) -> CreateAddressListResponseTypeDef:
        """
        Creates a new address list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/create_address_list.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#create_address_list)
        """

    def create_address_list_import_job(
        self, **kwargs: Unpack[CreateAddressListImportJobRequestRequestTypeDef]
    ) -> CreateAddressListImportJobResponseTypeDef:
        """
        Creates an import job for an address list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/create_address_list_import_job.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#create_address_list_import_job)
        """

    def create_archive(
        self, **kwargs: Unpack[CreateArchiveRequestRequestTypeDef]
    ) -> CreateArchiveResponseTypeDef:
        """
        Creates a new email archive resource for storing and retaining emails.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/create_archive.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#create_archive)
        """

    def create_ingress_point(
        self, **kwargs: Unpack[CreateIngressPointRequestRequestTypeDef]
    ) -> CreateIngressPointResponseTypeDef:
        """
        Provision a new ingress endpoint resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/create_ingress_point.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#create_ingress_point)
        """

    def create_relay(
        self, **kwargs: Unpack[CreateRelayRequestRequestTypeDef]
    ) -> CreateRelayResponseTypeDef:
        """
        Creates a relay resource which can be used in rules to relay incoming emails to
        defined relay destinations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/create_relay.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#create_relay)
        """

    def create_rule_set(
        self, **kwargs: Unpack[CreateRuleSetRequestRequestTypeDef]
    ) -> CreateRuleSetResponseTypeDef:
        """
        Provision a new rule set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/create_rule_set.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#create_rule_set)
        """

    def create_traffic_policy(
        self, **kwargs: Unpack[CreateTrafficPolicyRequestRequestTypeDef]
    ) -> CreateTrafficPolicyResponseTypeDef:
        """
        Provision a new traffic policy resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/create_traffic_policy.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#create_traffic_policy)
        """

    def delete_addon_instance(
        self, **kwargs: Unpack[DeleteAddonInstanceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an Add On instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/delete_addon_instance.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#delete_addon_instance)
        """

    def delete_addon_subscription(
        self, **kwargs: Unpack[DeleteAddonSubscriptionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an Add On subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/delete_addon_subscription.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#delete_addon_subscription)
        """

    def delete_address_list(
        self, **kwargs: Unpack[DeleteAddressListRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an address list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/delete_address_list.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#delete_address_list)
        """

    def delete_archive(
        self, **kwargs: Unpack[DeleteArchiveRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Initiates deletion of an email archive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/delete_archive.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#delete_archive)
        """

    def delete_ingress_point(
        self, **kwargs: Unpack[DeleteIngressPointRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Delete an ingress endpoint resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/delete_ingress_point.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#delete_ingress_point)
        """

    def delete_relay(self, **kwargs: Unpack[DeleteRelayRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes an existing relay resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/delete_relay.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#delete_relay)
        """

    def delete_rule_set(
        self, **kwargs: Unpack[DeleteRuleSetRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Delete a rule set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/delete_rule_set.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#delete_rule_set)
        """

    def delete_traffic_policy(
        self, **kwargs: Unpack[DeleteTrafficPolicyRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Delete a traffic policy resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/delete_traffic_policy.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#delete_traffic_policy)
        """

    def deregister_member_from_address_list(
        self, **kwargs: Unpack[DeregisterMemberFromAddressListRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes a member from an address list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/deregister_member_from_address_list.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#deregister_member_from_address_list)
        """

    def get_addon_instance(
        self, **kwargs: Unpack[GetAddonInstanceRequestRequestTypeDef]
    ) -> GetAddonInstanceResponseTypeDef:
        """
        Gets detailed information about an Add On instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_addon_instance.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#get_addon_instance)
        """

    def get_addon_subscription(
        self, **kwargs: Unpack[GetAddonSubscriptionRequestRequestTypeDef]
    ) -> GetAddonSubscriptionResponseTypeDef:
        """
        Gets detailed information about an Add On subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_addon_subscription.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#get_addon_subscription)
        """

    def get_address_list(
        self, **kwargs: Unpack[GetAddressListRequestRequestTypeDef]
    ) -> GetAddressListResponseTypeDef:
        """
        Fetch attributes of an address list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_address_list.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#get_address_list)
        """

    def get_address_list_import_job(
        self, **kwargs: Unpack[GetAddressListImportJobRequestRequestTypeDef]
    ) -> GetAddressListImportJobResponseTypeDef:
        """
        Fetch attributes of an import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_address_list_import_job.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#get_address_list_import_job)
        """

    def get_archive(
        self, **kwargs: Unpack[GetArchiveRequestRequestTypeDef]
    ) -> GetArchiveResponseTypeDef:
        """
        Retrieves the full details and current state of a specified email archive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_archive.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#get_archive)
        """

    def get_archive_export(
        self, **kwargs: Unpack[GetArchiveExportRequestRequestTypeDef]
    ) -> GetArchiveExportResponseTypeDef:
        """
        Retrieves the details and current status of a specific email archive export job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_archive_export.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#get_archive_export)
        """

    def get_archive_message(
        self, **kwargs: Unpack[GetArchiveMessageRequestRequestTypeDef]
    ) -> GetArchiveMessageResponseTypeDef:
        """
        Returns a pre-signed URL that provides temporary download access to the
        specific email message stored in the archive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_archive_message.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#get_archive_message)
        """

    def get_archive_message_content(
        self, **kwargs: Unpack[GetArchiveMessageContentRequestRequestTypeDef]
    ) -> GetArchiveMessageContentResponseTypeDef:
        """
        Returns the textual content of a specific email message stored in the archive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_archive_message_content.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#get_archive_message_content)
        """

    def get_archive_search(
        self, **kwargs: Unpack[GetArchiveSearchRequestRequestTypeDef]
    ) -> GetArchiveSearchResponseTypeDef:
        """
        Retrieves the details and current status of a specific email archive search job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_archive_search.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#get_archive_search)
        """

    def get_archive_search_results(
        self, **kwargs: Unpack[GetArchiveSearchResultsRequestRequestTypeDef]
    ) -> GetArchiveSearchResultsResponseTypeDef:
        """
        Returns the results of a completed email archive search job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_archive_search_results.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#get_archive_search_results)
        """

    def get_ingress_point(
        self, **kwargs: Unpack[GetIngressPointRequestRequestTypeDef]
    ) -> GetIngressPointResponseTypeDef:
        """
        Fetch ingress endpoint resource attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_ingress_point.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#get_ingress_point)
        """

    def get_member_of_address_list(
        self, **kwargs: Unpack[GetMemberOfAddressListRequestRequestTypeDef]
    ) -> GetMemberOfAddressListResponseTypeDef:
        """
        Fetch attributes of a member in an address list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_member_of_address_list.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#get_member_of_address_list)
        """

    def get_relay(self, **kwargs: Unpack[GetRelayRequestRequestTypeDef]) -> GetRelayResponseTypeDef:
        """
        Fetch the relay resource and it's attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_relay.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#get_relay)
        """

    def get_rule_set(
        self, **kwargs: Unpack[GetRuleSetRequestRequestTypeDef]
    ) -> GetRuleSetResponseTypeDef:
        """
        Fetch attributes of a rule set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_rule_set.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#get_rule_set)
        """

    def get_traffic_policy(
        self, **kwargs: Unpack[GetTrafficPolicyRequestRequestTypeDef]
    ) -> GetTrafficPolicyResponseTypeDef:
        """
        Fetch attributes of a traffic policy resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_traffic_policy.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#get_traffic_policy)
        """

    def list_addon_instances(
        self, **kwargs: Unpack[ListAddonInstancesRequestRequestTypeDef]
    ) -> ListAddonInstancesResponseTypeDef:
        """
        Lists all Add On instances in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/list_addon_instances.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#list_addon_instances)
        """

    def list_addon_subscriptions(
        self, **kwargs: Unpack[ListAddonSubscriptionsRequestRequestTypeDef]
    ) -> ListAddonSubscriptionsResponseTypeDef:
        """
        Lists all Add On subscriptions in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/list_addon_subscriptions.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#list_addon_subscriptions)
        """

    def list_address_list_import_jobs(
        self, **kwargs: Unpack[ListAddressListImportJobsRequestRequestTypeDef]
    ) -> ListAddressListImportJobsResponseTypeDef:
        """
        Lists jobs for an address list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/list_address_list_import_jobs.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#list_address_list_import_jobs)
        """

    def list_address_lists(
        self, **kwargs: Unpack[ListAddressListsRequestRequestTypeDef]
    ) -> ListAddressListsResponseTypeDef:
        """
        Lists address lists for this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/list_address_lists.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#list_address_lists)
        """

    def list_archive_exports(
        self, **kwargs: Unpack[ListArchiveExportsRequestRequestTypeDef]
    ) -> ListArchiveExportsResponseTypeDef:
        """
        Returns a list of email archive export jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/list_archive_exports.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#list_archive_exports)
        """

    def list_archive_searches(
        self, **kwargs: Unpack[ListArchiveSearchesRequestRequestTypeDef]
    ) -> ListArchiveSearchesResponseTypeDef:
        """
        Returns a list of email archive search jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/list_archive_searches.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#list_archive_searches)
        """

    def list_archives(
        self, **kwargs: Unpack[ListArchivesRequestRequestTypeDef]
    ) -> ListArchivesResponseTypeDef:
        """
        Returns a list of all email archives in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/list_archives.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#list_archives)
        """

    def list_ingress_points(
        self, **kwargs: Unpack[ListIngressPointsRequestRequestTypeDef]
    ) -> ListIngressPointsResponseTypeDef:
        """
        List all ingress endpoint resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/list_ingress_points.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#list_ingress_points)
        """

    def list_members_of_address_list(
        self, **kwargs: Unpack[ListMembersOfAddressListRequestRequestTypeDef]
    ) -> ListMembersOfAddressListResponseTypeDef:
        """
        Lists members of an address list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/list_members_of_address_list.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#list_members_of_address_list)
        """

    def list_relays(
        self, **kwargs: Unpack[ListRelaysRequestRequestTypeDef]
    ) -> ListRelaysResponseTypeDef:
        """
        Lists all the existing relay resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/list_relays.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#list_relays)
        """

    def list_rule_sets(
        self, **kwargs: Unpack[ListRuleSetsRequestRequestTypeDef]
    ) -> ListRuleSetsResponseTypeDef:
        """
        List rule sets for this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/list_rule_sets.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#list_rule_sets)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieves the list of tags (keys and values) assigned to the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/list_tags_for_resource.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#list_tags_for_resource)
        """

    def list_traffic_policies(
        self, **kwargs: Unpack[ListTrafficPoliciesRequestRequestTypeDef]
    ) -> ListTrafficPoliciesResponseTypeDef:
        """
        List traffic policy resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/list_traffic_policies.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#list_traffic_policies)
        """

    def register_member_to_address_list(
        self, **kwargs: Unpack[RegisterMemberToAddressListRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds a member to an address list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/register_member_to_address_list.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#register_member_to_address_list)
        """

    def start_address_list_import_job(
        self, **kwargs: Unpack[StartAddressListImportJobRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Starts an import job for an address list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/start_address_list_import_job.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#start_address_list_import_job)
        """

    def start_archive_export(
        self, **kwargs: Unpack[StartArchiveExportRequestRequestTypeDef]
    ) -> StartArchiveExportResponseTypeDef:
        """
        Initiates an export of emails from the specified archive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/start_archive_export.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#start_archive_export)
        """

    def start_archive_search(
        self, **kwargs: Unpack[StartArchiveSearchRequestRequestTypeDef]
    ) -> StartArchiveSearchResponseTypeDef:
        """
        Initiates a search across emails in the specified archive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/start_archive_search.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#start_archive_search)
        """

    def stop_address_list_import_job(
        self, **kwargs: Unpack[StopAddressListImportJobRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stops an ongoing import job for an address list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/stop_address_list_import_job.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#stop_address_list_import_job)
        """

    def stop_archive_export(
        self, **kwargs: Unpack[StopArchiveExportRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stops an in-progress export of emails from an archive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/stop_archive_export.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#stop_archive_export)
        """

    def stop_archive_search(
        self, **kwargs: Unpack[StopArchiveSearchRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stops an in-progress archive search job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/stop_archive_search.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#stop_archive_search)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds one or more tags (keys and values) to a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/tag_resource.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Remove one or more tags (keys and values) from a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/untag_resource.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#untag_resource)
        """

    def update_archive(
        self, **kwargs: Unpack[UpdateArchiveRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the attributes of an existing email archive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/update_archive.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#update_archive)
        """

    def update_ingress_point(
        self, **kwargs: Unpack[UpdateIngressPointRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Update attributes of a provisioned ingress endpoint resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/update_ingress_point.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#update_ingress_point)
        """

    def update_relay(self, **kwargs: Unpack[UpdateRelayRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Updates the attributes of an existing relay resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/update_relay.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#update_relay)
        """

    def update_rule_set(
        self, **kwargs: Unpack[UpdateRuleSetRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Update attributes of an already provisioned rule set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/update_rule_set.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#update_rule_set)
        """

    def update_traffic_policy(
        self, **kwargs: Unpack[UpdateTrafficPolicyRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Update attributes of an already provisioned traffic policy resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/update_traffic_policy.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#update_traffic_policy)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_addon_instances"]
    ) -> ListAddonInstancesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_addon_subscriptions"]
    ) -> ListAddonSubscriptionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_address_list_import_jobs"]
    ) -> ListAddressListImportJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_address_lists"]
    ) -> ListAddressListsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_archive_exports"]
    ) -> ListArchiveExportsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_archive_searches"]
    ) -> ListArchiveSearchesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_archives"]
    ) -> ListArchivesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_ingress_points"]
    ) -> ListIngressPointsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_members_of_address_list"]
    ) -> ListMembersOfAddressListPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_relays"]
    ) -> ListRelaysPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_rule_sets"]
    ) -> ListRuleSetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_traffic_policies"]
    ) -> ListTrafficPoliciesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/client/#get_paginator)
        """
