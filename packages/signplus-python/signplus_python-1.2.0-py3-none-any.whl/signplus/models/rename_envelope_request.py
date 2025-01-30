from .utils.json_map import JsonMap
from .utils.base_model import BaseModel


@JsonMap({})
class RenameEnvelopeRequest(BaseModel):
    """RenameEnvelopeRequest

    :param name: Name of the envelope, defaults to None
    :type name: str, optional
    """

    def __init__(self, name: str = None, **kwargs):
        """RenameEnvelopeRequest

        :param name: Name of the envelope, defaults to None
        :type name: str, optional
        """
        if name is not None:
            self.name = name
        self._kwargs = kwargs
