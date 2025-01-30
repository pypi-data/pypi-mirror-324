"""
Type annotations for pinpoint-email service Client.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_pinpoint_email.client import PinpointEmailClient

    session = Session()
    client: PinpointEmailClient = session.client("pinpoint-email")
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
    GetDedicatedIpsPaginator,
    ListConfigurationSetsPaginator,
    ListDedicatedIpPoolsPaginator,
    ListDeliverabilityTestReportsPaginator,
    ListEmailIdentitiesPaginator,
)
from .type_defs import (
    CreateConfigurationSetEventDestinationRequestRequestTypeDef,
    CreateConfigurationSetRequestRequestTypeDef,
    CreateDedicatedIpPoolRequestRequestTypeDef,
    CreateDeliverabilityTestReportRequestRequestTypeDef,
    CreateDeliverabilityTestReportResponseTypeDef,
    CreateEmailIdentityRequestRequestTypeDef,
    CreateEmailIdentityResponseTypeDef,
    DeleteConfigurationSetEventDestinationRequestRequestTypeDef,
    DeleteConfigurationSetRequestRequestTypeDef,
    DeleteDedicatedIpPoolRequestRequestTypeDef,
    DeleteEmailIdentityRequestRequestTypeDef,
    GetAccountResponseTypeDef,
    GetBlacklistReportsRequestRequestTypeDef,
    GetBlacklistReportsResponseTypeDef,
    GetConfigurationSetEventDestinationsRequestRequestTypeDef,
    GetConfigurationSetEventDestinationsResponseTypeDef,
    GetConfigurationSetRequestRequestTypeDef,
    GetConfigurationSetResponseTypeDef,
    GetDedicatedIpRequestRequestTypeDef,
    GetDedicatedIpResponseTypeDef,
    GetDedicatedIpsRequestRequestTypeDef,
    GetDedicatedIpsResponseTypeDef,
    GetDeliverabilityDashboardOptionsResponseTypeDef,
    GetDeliverabilityTestReportRequestRequestTypeDef,
    GetDeliverabilityTestReportResponseTypeDef,
    GetDomainDeliverabilityCampaignRequestRequestTypeDef,
    GetDomainDeliverabilityCampaignResponseTypeDef,
    GetDomainStatisticsReportRequestRequestTypeDef,
    GetDomainStatisticsReportResponseTypeDef,
    GetEmailIdentityRequestRequestTypeDef,
    GetEmailIdentityResponseTypeDef,
    ListConfigurationSetsRequestRequestTypeDef,
    ListConfigurationSetsResponseTypeDef,
    ListDedicatedIpPoolsRequestRequestTypeDef,
    ListDedicatedIpPoolsResponseTypeDef,
    ListDeliverabilityTestReportsRequestRequestTypeDef,
    ListDeliverabilityTestReportsResponseTypeDef,
    ListDomainDeliverabilityCampaignsRequestRequestTypeDef,
    ListDomainDeliverabilityCampaignsResponseTypeDef,
    ListEmailIdentitiesRequestRequestTypeDef,
    ListEmailIdentitiesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutAccountDedicatedIpWarmupAttributesRequestRequestTypeDef,
    PutAccountSendingAttributesRequestRequestTypeDef,
    PutConfigurationSetDeliveryOptionsRequestRequestTypeDef,
    PutConfigurationSetReputationOptionsRequestRequestTypeDef,
    PutConfigurationSetSendingOptionsRequestRequestTypeDef,
    PutConfigurationSetTrackingOptionsRequestRequestTypeDef,
    PutDedicatedIpInPoolRequestRequestTypeDef,
    PutDedicatedIpWarmupAttributesRequestRequestTypeDef,
    PutDeliverabilityDashboardOptionRequestRequestTypeDef,
    PutEmailIdentityDkimAttributesRequestRequestTypeDef,
    PutEmailIdentityFeedbackAttributesRequestRequestTypeDef,
    PutEmailIdentityMailFromAttributesRequestRequestTypeDef,
    SendEmailRequestRequestTypeDef,
    SendEmailResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateConfigurationSetEventDestinationRequestRequestTypeDef,
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


__all__ = ("PinpointEmailClient",)


class Exceptions(BaseClientExceptions):
    AccountSuspendedException: Type[BotocoreClientError]
    AlreadyExistsException: Type[BotocoreClientError]
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    MailFromDomainNotVerifiedException: Type[BotocoreClientError]
    MessageRejected: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    SendingPausedException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]


class PinpointEmailClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        PinpointEmailClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#generate_presigned_url)
        """

    def create_configuration_set(
        self, **kwargs: Unpack[CreateConfigurationSetRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Create a configuration set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/create_configuration_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#create_configuration_set)
        """

    def create_configuration_set_event_destination(
        self, **kwargs: Unpack[CreateConfigurationSetEventDestinationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Create an event destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/create_configuration_set_event_destination.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#create_configuration_set_event_destination)
        """

    def create_dedicated_ip_pool(
        self, **kwargs: Unpack[CreateDedicatedIpPoolRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Create a new pool of dedicated IP addresses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/create_dedicated_ip_pool.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#create_dedicated_ip_pool)
        """

    def create_deliverability_test_report(
        self, **kwargs: Unpack[CreateDeliverabilityTestReportRequestRequestTypeDef]
    ) -> CreateDeliverabilityTestReportResponseTypeDef:
        """
        Create a new predictive inbox placement test.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/create_deliverability_test_report.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#create_deliverability_test_report)
        """

    def create_email_identity(
        self, **kwargs: Unpack[CreateEmailIdentityRequestRequestTypeDef]
    ) -> CreateEmailIdentityResponseTypeDef:
        """
        Verifies an email identity for use with Amazon Pinpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/create_email_identity.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#create_email_identity)
        """

    def delete_configuration_set(
        self, **kwargs: Unpack[DeleteConfigurationSetRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Delete an existing configuration set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/delete_configuration_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#delete_configuration_set)
        """

    def delete_configuration_set_event_destination(
        self, **kwargs: Unpack[DeleteConfigurationSetEventDestinationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Delete an event destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/delete_configuration_set_event_destination.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#delete_configuration_set_event_destination)
        """

    def delete_dedicated_ip_pool(
        self, **kwargs: Unpack[DeleteDedicatedIpPoolRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Delete a dedicated IP pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/delete_dedicated_ip_pool.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#delete_dedicated_ip_pool)
        """

    def delete_email_identity(
        self, **kwargs: Unpack[DeleteEmailIdentityRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an email identity that you previously verified for use with Amazon
        Pinpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/delete_email_identity.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#delete_email_identity)
        """

    def get_account(self) -> GetAccountResponseTypeDef:
        """
        Obtain information about the email-sending status and capabilities of your
        Amazon Pinpoint account in the current AWS Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/get_account.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#get_account)
        """

    def get_blacklist_reports(
        self, **kwargs: Unpack[GetBlacklistReportsRequestRequestTypeDef]
    ) -> GetBlacklistReportsResponseTypeDef:
        """
        Retrieve a list of the blacklists that your dedicated IP addresses appear on.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/get_blacklist_reports.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#get_blacklist_reports)
        """

    def get_configuration_set(
        self, **kwargs: Unpack[GetConfigurationSetRequestRequestTypeDef]
    ) -> GetConfigurationSetResponseTypeDef:
        """
        Get information about an existing configuration set, including the dedicated IP
        pool that it's associated with, whether or not it's enabled for sending email,
        and more.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/get_configuration_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#get_configuration_set)
        """

    def get_configuration_set_event_destinations(
        self, **kwargs: Unpack[GetConfigurationSetEventDestinationsRequestRequestTypeDef]
    ) -> GetConfigurationSetEventDestinationsResponseTypeDef:
        """
        Retrieve a list of event destinations that are associated with a configuration
        set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/get_configuration_set_event_destinations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#get_configuration_set_event_destinations)
        """

    def get_dedicated_ip(
        self, **kwargs: Unpack[GetDedicatedIpRequestRequestTypeDef]
    ) -> GetDedicatedIpResponseTypeDef:
        """
        Get information about a dedicated IP address, including the name of the
        dedicated IP pool that it's associated with, as well information about the
        automatic warm-up process for the address.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/get_dedicated_ip.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#get_dedicated_ip)
        """

    def get_dedicated_ips(
        self, **kwargs: Unpack[GetDedicatedIpsRequestRequestTypeDef]
    ) -> GetDedicatedIpsResponseTypeDef:
        """
        List the dedicated IP addresses that are associated with your Amazon Pinpoint
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/get_dedicated_ips.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#get_dedicated_ips)
        """

    def get_deliverability_dashboard_options(
        self,
    ) -> GetDeliverabilityDashboardOptionsResponseTypeDef:
        """
        Retrieve information about the status of the Deliverability dashboard for your
        Amazon Pinpoint account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/get_deliverability_dashboard_options.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#get_deliverability_dashboard_options)
        """

    def get_deliverability_test_report(
        self, **kwargs: Unpack[GetDeliverabilityTestReportRequestRequestTypeDef]
    ) -> GetDeliverabilityTestReportResponseTypeDef:
        """
        Retrieve the results of a predictive inbox placement test.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/get_deliverability_test_report.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#get_deliverability_test_report)
        """

    def get_domain_deliverability_campaign(
        self, **kwargs: Unpack[GetDomainDeliverabilityCampaignRequestRequestTypeDef]
    ) -> GetDomainDeliverabilityCampaignResponseTypeDef:
        """
        Retrieve all the deliverability data for a specific campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/get_domain_deliverability_campaign.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#get_domain_deliverability_campaign)
        """

    def get_domain_statistics_report(
        self, **kwargs: Unpack[GetDomainStatisticsReportRequestRequestTypeDef]
    ) -> GetDomainStatisticsReportResponseTypeDef:
        """
        Retrieve inbox placement and engagement rates for the domains that you use to
        send email.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/get_domain_statistics_report.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#get_domain_statistics_report)
        """

    def get_email_identity(
        self, **kwargs: Unpack[GetEmailIdentityRequestRequestTypeDef]
    ) -> GetEmailIdentityResponseTypeDef:
        """
        Provides information about a specific identity associated with your Amazon
        Pinpoint account, including the identity's verification status, its DKIM
        authentication status, and its custom Mail-From settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/get_email_identity.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#get_email_identity)
        """

    def list_configuration_sets(
        self, **kwargs: Unpack[ListConfigurationSetsRequestRequestTypeDef]
    ) -> ListConfigurationSetsResponseTypeDef:
        """
        List all of the configuration sets associated with your Amazon Pinpoint account
        in the current region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/list_configuration_sets.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#list_configuration_sets)
        """

    def list_dedicated_ip_pools(
        self, **kwargs: Unpack[ListDedicatedIpPoolsRequestRequestTypeDef]
    ) -> ListDedicatedIpPoolsResponseTypeDef:
        """
        List all of the dedicated IP pools that exist in your Amazon Pinpoint account
        in the current AWS Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/list_dedicated_ip_pools.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#list_dedicated_ip_pools)
        """

    def list_deliverability_test_reports(
        self, **kwargs: Unpack[ListDeliverabilityTestReportsRequestRequestTypeDef]
    ) -> ListDeliverabilityTestReportsResponseTypeDef:
        """
        Show a list of the predictive inbox placement tests that you've performed,
        regardless of their statuses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/list_deliverability_test_reports.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#list_deliverability_test_reports)
        """

    def list_domain_deliverability_campaigns(
        self, **kwargs: Unpack[ListDomainDeliverabilityCampaignsRequestRequestTypeDef]
    ) -> ListDomainDeliverabilityCampaignsResponseTypeDef:
        """
        Retrieve deliverability data for all the campaigns that used a specific domain
        to send email during a specified time range.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/list_domain_deliverability_campaigns.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#list_domain_deliverability_campaigns)
        """

    def list_email_identities(
        self, **kwargs: Unpack[ListEmailIdentitiesRequestRequestTypeDef]
    ) -> ListEmailIdentitiesResponseTypeDef:
        """
        Returns a list of all of the email identities that are associated with your
        Amazon Pinpoint account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/list_email_identities.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#list_email_identities)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieve a list of the tags (keys and values) that are associated with a
        specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#list_tags_for_resource)
        """

    def put_account_dedicated_ip_warmup_attributes(
        self, **kwargs: Unpack[PutAccountDedicatedIpWarmupAttributesRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Enable or disable the automatic warm-up feature for dedicated IP addresses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/put_account_dedicated_ip_warmup_attributes.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#put_account_dedicated_ip_warmup_attributes)
        """

    def put_account_sending_attributes(
        self, **kwargs: Unpack[PutAccountSendingAttributesRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Enable or disable the ability of your account to send email.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/put_account_sending_attributes.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#put_account_sending_attributes)
        """

    def put_configuration_set_delivery_options(
        self, **kwargs: Unpack[PutConfigurationSetDeliveryOptionsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associate a configuration set with a dedicated IP pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/put_configuration_set_delivery_options.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#put_configuration_set_delivery_options)
        """

    def put_configuration_set_reputation_options(
        self, **kwargs: Unpack[PutConfigurationSetReputationOptionsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Enable or disable collection of reputation metrics for emails that you send
        using a particular configuration set in a specific AWS Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/put_configuration_set_reputation_options.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#put_configuration_set_reputation_options)
        """

    def put_configuration_set_sending_options(
        self, **kwargs: Unpack[PutConfigurationSetSendingOptionsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Enable or disable email sending for messages that use a particular
        configuration set in a specific AWS Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/put_configuration_set_sending_options.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#put_configuration_set_sending_options)
        """

    def put_configuration_set_tracking_options(
        self, **kwargs: Unpack[PutConfigurationSetTrackingOptionsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Specify a custom domain to use for open and click tracking elements in email
        that you send using Amazon Pinpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/put_configuration_set_tracking_options.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#put_configuration_set_tracking_options)
        """

    def put_dedicated_ip_in_pool(
        self, **kwargs: Unpack[PutDedicatedIpInPoolRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Move a dedicated IP address to an existing dedicated IP pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/put_dedicated_ip_in_pool.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#put_dedicated_ip_in_pool)
        """

    def put_dedicated_ip_warmup_attributes(
        self, **kwargs: Unpack[PutDedicatedIpWarmupAttributesRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        <p/>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/put_dedicated_ip_warmup_attributes.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#put_dedicated_ip_warmup_attributes)
        """

    def put_deliverability_dashboard_option(
        self, **kwargs: Unpack[PutDeliverabilityDashboardOptionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Enable or disable the Deliverability dashboard for your Amazon Pinpoint account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/put_deliverability_dashboard_option.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#put_deliverability_dashboard_option)
        """

    def put_email_identity_dkim_attributes(
        self, **kwargs: Unpack[PutEmailIdentityDkimAttributesRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Used to enable or disable DKIM authentication for an email identity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/put_email_identity_dkim_attributes.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#put_email_identity_dkim_attributes)
        """

    def put_email_identity_feedback_attributes(
        self, **kwargs: Unpack[PutEmailIdentityFeedbackAttributesRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Used to enable or disable feedback forwarding for an identity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/put_email_identity_feedback_attributes.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#put_email_identity_feedback_attributes)
        """

    def put_email_identity_mail_from_attributes(
        self, **kwargs: Unpack[PutEmailIdentityMailFromAttributesRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Used to enable or disable the custom Mail-From domain configuration for an
        email identity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/put_email_identity_mail_from_attributes.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#put_email_identity_mail_from_attributes)
        """

    def send_email(
        self, **kwargs: Unpack[SendEmailRequestRequestTypeDef]
    ) -> SendEmailResponseTypeDef:
        """
        Sends an email message.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/send_email.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#send_email)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Add one or more tags (keys and values) to a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Remove one or more tags (keys and values) from a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#untag_resource)
        """

    def update_configuration_set_event_destination(
        self, **kwargs: Unpack[UpdateConfigurationSetEventDestinationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Update the configuration of an event destination for a configuration set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/update_configuration_set_event_destination.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#update_configuration_set_event_destination)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_dedicated_ips"]
    ) -> GetDedicatedIpsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_configuration_sets"]
    ) -> ListConfigurationSetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_dedicated_ip_pools"]
    ) -> ListDedicatedIpPoolsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_deliverability_test_reports"]
    ) -> ListDeliverabilityTestReportsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_email_identities"]
    ) -> ListEmailIdentitiesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_email/client/#get_paginator)
        """
