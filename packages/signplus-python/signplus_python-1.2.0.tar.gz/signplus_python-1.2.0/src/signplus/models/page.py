from .utils.json_map import JsonMap
from .utils.base_model import BaseModel


@JsonMap({})
class Page(BaseModel):
    """Page

    :param width: Width of the page in pixels, defaults to None
    :type width: int, optional
    :param height: Height of the page in pixels, defaults to None
    :type height: int, optional
    """

    def __init__(self, width: int = None, height: int = None, **kwargs):
        """Page

        :param width: Width of the page in pixels, defaults to None
        :type width: int, optional
        :param height: Height of the page in pixels, defaults to None
        :type height: int, optional
        """
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
        self._kwargs = kwargs
