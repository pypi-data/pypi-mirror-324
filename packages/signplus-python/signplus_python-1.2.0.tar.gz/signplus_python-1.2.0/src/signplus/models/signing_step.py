from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .utils.base_model import BaseModel
from .recipient import Recipient


@JsonMap({})
class SigningStep(BaseModel):
    """SigningStep

    :param recipients: List of recipients, defaults to None
    :type recipients: List[Recipient], optional
    """

    def __init__(self, recipients: List[Recipient] = None, **kwargs):
        """SigningStep

        :param recipients: List of recipients, defaults to None
        :type recipients: List[Recipient], optional
        """
        if recipients is not None:
            self.recipients = self._define_list(recipients, Recipient)
        self._kwargs = kwargs
