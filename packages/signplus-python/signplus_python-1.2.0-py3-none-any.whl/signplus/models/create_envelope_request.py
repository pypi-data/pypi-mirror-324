from __future__ import annotations
from .utils.json_map import JsonMap
from .utils.base_model import BaseModel
from .envelope_legality_level import EnvelopeLegalityLevel


@JsonMap({})
class CreateEnvelopeRequest(BaseModel):
    """CreateEnvelopeRequest

    :param name: Name of the envelope
    :type name: str
    :param legality_level: Legal level of the envelope (SES is Simple Electronic Signature, QES_EIDAS is Qualified Electronic Signature, QES_ZERTES is Qualified Electronic Signature with Zertes)
    :type legality_level: EnvelopeLegalityLevel
    :param expires_at: Unix timestamp of the expiration date, defaults to None
    :type expires_at: int, optional
    :param comment: Comment for the envelope, defaults to None
    :type comment: str, optional
    :param sandbox: Whether the envelope is created in sandbox mode, defaults to None
    :type sandbox: bool, optional
    """

    def __init__(
        self,
        name: str,
        legality_level: EnvelopeLegalityLevel,
        expires_at: int = None,
        comment: str = None,
        sandbox: bool = None,
        **kwargs,
    ):
        """CreateEnvelopeRequest

        :param name: Name of the envelope
        :type name: str
        :param legality_level: Legal level of the envelope (SES is Simple Electronic Signature, QES_EIDAS is Qualified Electronic Signature, QES_ZERTES is Qualified Electronic Signature with Zertes)
        :type legality_level: EnvelopeLegalityLevel
        :param expires_at: Unix timestamp of the expiration date, defaults to None
        :type expires_at: int, optional
        :param comment: Comment for the envelope, defaults to None
        :type comment: str, optional
        :param sandbox: Whether the envelope is created in sandbox mode, defaults to None
        :type sandbox: bool, optional
        """
        self.name = name
        self.legality_level = self._enum_matching(
            legality_level, EnvelopeLegalityLevel.list(), "legality_level"
        )
        if expires_at is not None:
            self.expires_at = expires_at
        if comment is not None:
            self.comment = comment
        if sandbox is not None:
            self.sandbox = sandbox
        self._kwargs = kwargs
