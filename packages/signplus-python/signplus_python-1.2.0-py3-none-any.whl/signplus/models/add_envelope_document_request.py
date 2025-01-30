from .utils.json_map import JsonMap
from .utils.base_model import BaseModel


@JsonMap({})
class AddEnvelopeDocumentRequest(BaseModel):
    """AddEnvelopeDocumentRequest

    :param file: File to upload in binary format, defaults to None
    :type file: bytes, optional
    """

    def __init__(self, file: bytes = None, **kwargs):
        """AddEnvelopeDocumentRequest

        :param file: File to upload in binary format, defaults to None
        :type file: bytes, optional
        """
        if file is not None:
            self.file = file
        self._kwargs = kwargs
