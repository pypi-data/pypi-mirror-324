from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .utils.base_model import BaseModel
from .document import Document


@JsonMap({})
class ListTemplateDocumentsResponse(BaseModel):
    """ListTemplateDocumentsResponse

    :param documents: documents, defaults to None
    :type documents: List[Document], optional
    """

    def __init__(self, documents: List[Document] = None, **kwargs):
        """ListTemplateDocumentsResponse

        :param documents: documents, defaults to None
        :type documents: List[Document], optional
        """
        if documents is not None:
            self.documents = self._define_list(documents, Document)
        self._kwargs = kwargs
