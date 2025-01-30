from .utils.json_map import JsonMap
from .utils.base_model import BaseModel


@JsonMap({})
class CreateTemplateRequest(BaseModel):
    """CreateTemplateRequest

    :param name: name
    :type name: str
    """

    def __init__(self, name: str, **kwargs):
        """CreateTemplateRequest

        :param name: name
        :type name: str
        """
        self.name = name
        self._kwargs = kwargs
