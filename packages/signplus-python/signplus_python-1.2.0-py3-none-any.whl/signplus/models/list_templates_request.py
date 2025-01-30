from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .utils.base_model import BaseModel
from .template_order_field import TemplateOrderField


@JsonMap({})
class ListTemplatesRequest(BaseModel):
    """ListTemplatesRequest

    :param name: Name of the template, defaults to None
    :type name: str, optional
    :param tags: List of tag templates, defaults to None
    :type tags: List[str], optional
    :param ids: List of templates IDs, defaults to None
    :type ids: List[str], optional
    :param first: first, defaults to None
    :type first: int, optional
    :param last: last, defaults to None
    :type last: int, optional
    :param after: after, defaults to None
    :type after: str, optional
    :param before: before, defaults to None
    :type before: str, optional
    :param order_field: Field to order templates by, defaults to None
    :type order_field: TemplateOrderField, optional
    :param ascending: Whether to order templates in ascending order, defaults to None
    :type ascending: bool, optional
    """

    def __init__(
        self,
        name: str = None,
        tags: List[str] = None,
        ids: List[str] = None,
        first: int = None,
        last: int = None,
        after: str = None,
        before: str = None,
        order_field: TemplateOrderField = None,
        ascending: bool = None,
        **kwargs,
    ):
        """ListTemplatesRequest

        :param name: Name of the template, defaults to None
        :type name: str, optional
        :param tags: List of tag templates, defaults to None
        :type tags: List[str], optional
        :param ids: List of templates IDs, defaults to None
        :type ids: List[str], optional
        :param first: first, defaults to None
        :type first: int, optional
        :param last: last, defaults to None
        :type last: int, optional
        :param after: after, defaults to None
        :type after: str, optional
        :param before: before, defaults to None
        :type before: str, optional
        :param order_field: Field to order templates by, defaults to None
        :type order_field: TemplateOrderField, optional
        :param ascending: Whether to order templates in ascending order, defaults to None
        :type ascending: bool, optional
        """
        if name is not None:
            self.name = name
        if tags is not None:
            self.tags = tags
        if ids is not None:
            self.ids = ids
        if first is not None:
            self.first = first
        if last is not None:
            self.last = last
        if after is not None:
            self.after = after
        if before is not None:
            self.before = before
        if order_field is not None:
            self.order_field = self._enum_matching(
                order_field, TemplateOrderField.list(), "order_field"
            )
        if ascending is not None:
            self.ascending = ascending
        self._kwargs = kwargs
