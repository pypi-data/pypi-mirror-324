from .utils.json_map import JsonMap
from .utils.base_model import BaseModel


@JsonMap({})
class CreateEnvelopeFromTemplateRequest(BaseModel):
    """CreateEnvelopeFromTemplateRequest

    :param name: Name of the envelope
    :type name: str
    :param comment: Comment for the envelope, defaults to None
    :type comment: str, optional
    :param sandbox: Whether the envelope is created in sandbox mode, defaults to None
    :type sandbox: bool, optional
    """

    def __init__(self, name: str, comment: str = None, sandbox: bool = None, **kwargs):
        """CreateEnvelopeFromTemplateRequest

        :param name: Name of the envelope
        :type name: str
        :param comment: Comment for the envelope, defaults to None
        :type comment: str, optional
        :param sandbox: Whether the envelope is created in sandbox mode, defaults to None
        :type sandbox: bool, optional
        """
        self.name = name
        if comment is not None:
            self.comment = comment
        if sandbox is not None:
            self.sandbox = sandbox
        self._kwargs = kwargs
