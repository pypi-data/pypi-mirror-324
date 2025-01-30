from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .utils.base_model import BaseModel
from .envelope_legality_level import EnvelopeLegalityLevel
from .template_signing_step import TemplateSigningStep
from .document import Document
from .envelope_notification import EnvelopeNotification


@JsonMap({"id_": "id"})
class Template(BaseModel):
    """Template

    :param id_: Unique identifier of the template, defaults to None
    :type id_: str, optional
    :param name: Name of the template, defaults to None
    :type name: str, optional
    :param comment: Comment for the template, defaults to None
    :type comment: str, optional
    :param pages: Total number of pages in the template, defaults to None
    :type pages: int, optional
    :param legality_level: Legal level of the envelope (SES is Simple Electronic Signature, QES_EIDAS is Qualified Electronic Signature, QES_ZERTES is Qualified Electronic Signature with Zertes), defaults to None
    :type legality_level: EnvelopeLegalityLevel, optional
    :param created_at: Unix timestamp of the creation date, defaults to None
    :type created_at: int, optional
    :param updated_at: Unix timestamp of the last modification date, defaults to None
    :type updated_at: int, optional
    :param expiration_delay: Expiration delay added to the current time when an envelope is created from this template, defaults to None
    :type expiration_delay: int, optional
    :param num_recipients: Number of recipients in the envelope, defaults to None
    :type num_recipients: int, optional
    :param signing_steps: signing_steps, defaults to None
    :type signing_steps: List[TemplateSigningStep], optional
    :param documents: documents, defaults to None
    :type documents: List[Document], optional
    :param notification: notification, defaults to None
    :type notification: EnvelopeNotification, optional
    :param dynamic_fields: List of dynamic fields, defaults to None
    :type dynamic_fields: List[str], optional
    """

    def __init__(
        self,
        id_: str = None,
        name: str = None,
        comment: str = None,
        pages: int = None,
        legality_level: EnvelopeLegalityLevel = None,
        created_at: int = None,
        updated_at: int = None,
        expiration_delay: int = None,
        num_recipients: int = None,
        signing_steps: List[TemplateSigningStep] = None,
        documents: List[Document] = None,
        notification: EnvelopeNotification = None,
        dynamic_fields: List[str] = None,
        **kwargs,
    ):
        """Template

        :param id_: Unique identifier of the template, defaults to None
        :type id_: str, optional
        :param name: Name of the template, defaults to None
        :type name: str, optional
        :param comment: Comment for the template, defaults to None
        :type comment: str, optional
        :param pages: Total number of pages in the template, defaults to None
        :type pages: int, optional
        :param legality_level: Legal level of the envelope (SES is Simple Electronic Signature, QES_EIDAS is Qualified Electronic Signature, QES_ZERTES is Qualified Electronic Signature with Zertes), defaults to None
        :type legality_level: EnvelopeLegalityLevel, optional
        :param created_at: Unix timestamp of the creation date, defaults to None
        :type created_at: int, optional
        :param updated_at: Unix timestamp of the last modification date, defaults to None
        :type updated_at: int, optional
        :param expiration_delay: Expiration delay added to the current time when an envelope is created from this template, defaults to None
        :type expiration_delay: int, optional
        :param num_recipients: Number of recipients in the envelope, defaults to None
        :type num_recipients: int, optional
        :param signing_steps: signing_steps, defaults to None
        :type signing_steps: List[TemplateSigningStep], optional
        :param documents: documents, defaults to None
        :type documents: List[Document], optional
        :param notification: notification, defaults to None
        :type notification: EnvelopeNotification, optional
        :param dynamic_fields: List of dynamic fields, defaults to None
        :type dynamic_fields: List[str], optional
        """
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name
        if comment is not None:
            self.comment = comment
        if pages is not None:
            self.pages = pages
        if legality_level is not None:
            self.legality_level = self._enum_matching(
                legality_level, EnvelopeLegalityLevel.list(), "legality_level"
            )
        if created_at is not None:
            self.created_at = created_at
        if updated_at is not None:
            self.updated_at = updated_at
        if expiration_delay is not None:
            self.expiration_delay = expiration_delay
        if num_recipients is not None:
            self.num_recipients = num_recipients
        if signing_steps is not None:
            self.signing_steps = self._define_list(signing_steps, TemplateSigningStep)
        if documents is not None:
            self.documents = self._define_list(documents, Document)
        if notification is not None:
            self.notification = self._define_object(notification, EnvelopeNotification)
        if dynamic_fields is not None:
            self.dynamic_fields = dynamic_fields
        self._kwargs = kwargs
