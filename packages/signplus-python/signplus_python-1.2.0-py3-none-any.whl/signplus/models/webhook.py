from __future__ import annotations
from .utils.json_map import JsonMap
from .utils.base_model import BaseModel
from .webhook_event import WebhookEvent


@JsonMap({"id_": "id"})
class Webhook(BaseModel):
    """Webhook

    :param id_: Unique identifier of the webhook, defaults to None
    :type id_: str, optional
    :param event: Event of the webhook, defaults to None
    :type event: WebhookEvent, optional
    :param target: Target URL of the webhook, defaults to None
    :type target: str, optional
    """

    def __init__(
        self, id_: str = None, event: WebhookEvent = None, target: str = None, **kwargs
    ):
        """Webhook

        :param id_: Unique identifier of the webhook, defaults to None
        :type id_: str, optional
        :param event: Event of the webhook, defaults to None
        :type event: WebhookEvent, optional
        :param target: Target URL of the webhook, defaults to None
        :type target: str, optional
        """
        if id_ is not None:
            self.id_ = id_
        if event is not None:
            self.event = self._enum_matching(event, WebhookEvent.list(), "event")
        if target is not None:
            self.target = target
        self._kwargs = kwargs
