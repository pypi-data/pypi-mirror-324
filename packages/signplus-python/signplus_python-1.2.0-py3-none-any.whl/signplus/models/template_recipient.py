from __future__ import annotations
from .utils.json_map import JsonMap
from .utils.base_model import BaseModel
from .template_recipient_role import TemplateRecipientRole


@JsonMap({"id_": "id"})
class TemplateRecipient(BaseModel):
    """TemplateRecipient

    :param id_: Unique identifier of the recipient, defaults to None
    :type id_: str, optional
    :param uid: Unique identifier of the user associated with the recipient, defaults to None
    :type uid: str, optional
    :param name: Name of the recipient, defaults to None
    :type name: str, optional
    :param email: Email of the recipient, defaults to None
    :type email: str, optional
    :param role: Role of the recipient (SIGNER signs the document, RECEIVES_COPY receives a copy of the document, IN_PERSON_SIGNER signs the document in person, SENDER sends the document), defaults to None
    :type role: TemplateRecipientRole, optional
    """

    def __init__(
        self,
        id_: str = None,
        uid: str = None,
        name: str = None,
        email: str = None,
        role: TemplateRecipientRole = None,
        **kwargs,
    ):
        """TemplateRecipient

        :param id_: Unique identifier of the recipient, defaults to None
        :type id_: str, optional
        :param uid: Unique identifier of the user associated with the recipient, defaults to None
        :type uid: str, optional
        :param name: Name of the recipient, defaults to None
        :type name: str, optional
        :param email: Email of the recipient, defaults to None
        :type email: str, optional
        :param role: Role of the recipient (SIGNER signs the document, RECEIVES_COPY receives a copy of the document, IN_PERSON_SIGNER signs the document in person, SENDER sends the document), defaults to None
        :type role: TemplateRecipientRole, optional
        """
        if id_ is not None:
            self.id_ = id_
        if uid is not None:
            self.uid = uid
        if name is not None:
            self.name = name
        if email is not None:
            self.email = email
        if role is not None:
            self.role = self._enum_matching(role, TemplateRecipientRole.list(), "role")
        self._kwargs = kwargs
