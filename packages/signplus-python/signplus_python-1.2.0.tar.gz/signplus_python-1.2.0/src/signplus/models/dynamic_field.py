from .utils.json_map import JsonMap
from .utils.base_model import BaseModel


@JsonMap({})
class DynamicField(BaseModel):
    """DynamicField

    :param name: Name of the dynamic field, defaults to None
    :type name: str, optional
    :param value: Value of the dynamic field, defaults to None
    :type value: str, optional
    """

    def __init__(self, name: str = None, value: str = None, **kwargs):
        """DynamicField

        :param name: Name of the dynamic field, defaults to None
        :type name: str, optional
        :param value: Value of the dynamic field, defaults to None
        :type value: str, optional
        """
        if name is not None:
            self.name = name
        if value is not None:
            self.value = value
        self._kwargs = kwargs
