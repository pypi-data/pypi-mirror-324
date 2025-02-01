from __future__ import annotations

from typing import TYPE_CHECKING

from oarepo_requests.actions.generic import OARepoAcceptAction
from oarepo_requests.types import ModelRefTypes
from oarepo_requests.types.generic import OARepoRequestType
from oarepo_runtime.datastreams.utils import get_record_service_for_record
from oarepo_runtime.i18n import lazy_gettext as _

from ..errors import CommunityAlreadyIncludedException
from ..proxies import current_oarepo_communities

if TYPE_CHECKING:
    from typing import Any

    from flask_principal import Identity
    from invenio_records_resources.records import Record
    from invenio_records_resources.services.uow import UnitOfWork
    from invenio_requests.customizations import RequestType
    from invenio_requests.customizations.actions import RequestAction
    from oarepo_requests.typing import EntityReference


class CommunitySubmissionAcceptAction(OARepoAcceptAction):

    def apply(
        self,
        identity: Identity,
        request_type: RequestType,
        topic: Any,
        uow: UnitOfWork,
        *args: Any,
        **kwargs: Any,
    ) -> None:

        community_id = self.request.receiver.resolve().community_id
        service = get_record_service_for_record(topic)
        community_inclusion_service = (
            current_oarepo_communities.community_inclusion_service
        )
        community_inclusion_service.include(
            topic, community_id, record_service=service, uow=uow, default=False
        )


class SecondaryCommunitySubmissionRequestType(OARepoRequestType):
    """Review request for submitting a record to a community."""

    type_id = "secondary_community_submission"
    name = _("Secondary community submission")
    allowed_topic_ref_types = ModelRefTypes(published=True, draft=True)

    @classmethod
    @property
    def available_actions(cls) -> dict[str, type[RequestAction]]:
        return {
            **super().available_actions,
            "accept": CommunitySubmissionAcceptAction,
        }

    def can_create(
        self,
        identity: Identity,
        data: dict,
        receiver: EntityReference,
        topic: Record,
        creator: EntityReference,
        *args: Any,
        **kwargs: Any,
    ) -> None:

        super().can_create(identity, data, receiver, topic, creator, *args, **kwargs)
        target_community_id = data["payload"]["community"]

        already_included = target_community_id in topic.parent.communities.ids
        if already_included:
            raise CommunityAlreadyIncludedException(
                "Record is already included in this community."
            )
