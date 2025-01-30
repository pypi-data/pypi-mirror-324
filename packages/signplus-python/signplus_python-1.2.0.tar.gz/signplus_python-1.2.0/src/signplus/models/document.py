from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .utils.base_model import BaseModel
from .page import Page


@JsonMap({"id_": "id"})
class Document(BaseModel):
    """Document

    :param id_: Unique identifier of the document, defaults to None
    :type id_: str, optional
    :param name: Name of the document, defaults to None
    :type name: str, optional
    :param filename: Filename of the document, defaults to None
    :type filename: str, optional
    :param page_count: Number of pages in the document, defaults to None
    :type page_count: int, optional
    :param pages: List of pages in the document, defaults to None
    :type pages: List[Page], optional
    """

    def __init__(
        self,
        id_: str = None,
        name: str = None,
        filename: str = None,
        page_count: int = None,
        pages: List[Page] = None,
        **kwargs,
    ):
        """Document

        :param id_: Unique identifier of the document, defaults to None
        :type id_: str, optional
        :param name: Name of the document, defaults to None
        :type name: str, optional
        :param filename: Filename of the document, defaults to None
        :type filename: str, optional
        :param page_count: Number of pages in the document, defaults to None
        :type page_count: int, optional
        :param pages: List of pages in the document, defaults to None
        :type pages: List[Page], optional
        """
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name
        if filename is not None:
            self.filename = filename
        if page_count is not None:
            self.page_count = page_count
        if pages is not None:
            self.pages = self._define_list(pages, Page)
        self._kwargs = kwargs
