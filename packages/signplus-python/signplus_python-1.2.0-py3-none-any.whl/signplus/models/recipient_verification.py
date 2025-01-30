from __future__ import annotations
from .utils.json_map import JsonMap
from .utils.base_model import BaseModel
from .recipient_verification_type import RecipientVerificationType


@JsonMap({"type_": "type"})
class RecipientVerification(BaseModel):
    """RecipientVerification

    :param type_: Type of signature verification (SMS sends a code via SMS, PASSCODE requires a code to be entered), defaults to None
    :type type_: RecipientVerificationType, optional
    :param value: value, defaults to None
    :type value: str, optional
    """

    def __init__(
        self, type_: RecipientVerificationType = None, value: str = None, **kwargs
    ):
        """RecipientVerification

        :param type_: Type of signature verification (SMS sends a code via SMS, PASSCODE requires a code to be entered), defaults to None
        :type type_: RecipientVerificationType, optional
        :param value: value, defaults to None
        :type value: str, optional
        """
        if type_ is not None:
            self.type_ = self._enum_matching(
                type_, RecipientVerificationType.list(), "type_"
            )
        if value is not None:
            self.value = value
        self._kwargs = kwargs
