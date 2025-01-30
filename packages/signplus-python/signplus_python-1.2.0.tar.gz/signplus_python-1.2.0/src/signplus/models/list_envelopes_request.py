from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .utils.base_model import BaseModel
from .envelope_status import EnvelopeStatus
from .envelope_order_field import EnvelopeOrderField


@JsonMap({})
class ListEnvelopesRequest(BaseModel):
    """ListEnvelopesRequest

    :param name: Name of the envelope, defaults to None
    :type name: str, optional
    :param tags: List of tags, defaults to None
    :type tags: List[str], optional
    :param comment: Comment of the envelope, defaults to None
    :type comment: str, optional
    :param ids: List of envelope IDs, defaults to None
    :type ids: List[str], optional
    :param statuses: List of envelope statuses, defaults to None
    :type statuses: List[EnvelopeStatus], optional
    :param folder_ids: List of folder IDs, defaults to None
    :type folder_ids: List[str], optional
    :param only_root_folder: Whether to only list envelopes in the root folder, defaults to None
    :type only_root_folder: bool, optional
    :param date_from: Unix timestamp of the start date, defaults to None
    :type date_from: int, optional
    :param date_to: Unix timestamp of the end date, defaults to None
    :type date_to: int, optional
    :param uid: Unique identifier of the user, defaults to None
    :type uid: str, optional
    :param first: first, defaults to None
    :type first: int, optional
    :param last: last, defaults to None
    :type last: int, optional
    :param after: after, defaults to None
    :type after: str, optional
    :param before: before, defaults to None
    :type before: str, optional
    :param order_field: Field to order envelopes by, defaults to None
    :type order_field: EnvelopeOrderField, optional
    :param ascending: Whether to order envelopes in ascending order, defaults to None
    :type ascending: bool, optional
    :param include_trash: Whether to include envelopes in the trash, defaults to None
    :type include_trash: bool, optional
    """

    def __init__(
        self,
        name: str = None,
        tags: List[str] = None,
        comment: str = None,
        ids: List[str] = None,
        statuses: List[EnvelopeStatus] = None,
        folder_ids: List[str] = None,
        only_root_folder: bool = None,
        date_from: int = None,
        date_to: int = None,
        uid: str = None,
        first: int = None,
        last: int = None,
        after: str = None,
        before: str = None,
        order_field: EnvelopeOrderField = None,
        ascending: bool = None,
        include_trash: bool = None,
        **kwargs,
    ):
        """ListEnvelopesRequest

        :param name: Name of the envelope, defaults to None
        :type name: str, optional
        :param tags: List of tags, defaults to None
        :type tags: List[str], optional
        :param comment: Comment of the envelope, defaults to None
        :type comment: str, optional
        :param ids: List of envelope IDs, defaults to None
        :type ids: List[str], optional
        :param statuses: List of envelope statuses, defaults to None
        :type statuses: List[EnvelopeStatus], optional
        :param folder_ids: List of folder IDs, defaults to None
        :type folder_ids: List[str], optional
        :param only_root_folder: Whether to only list envelopes in the root folder, defaults to None
        :type only_root_folder: bool, optional
        :param date_from: Unix timestamp of the start date, defaults to None
        :type date_from: int, optional
        :param date_to: Unix timestamp of the end date, defaults to None
        :type date_to: int, optional
        :param uid: Unique identifier of the user, defaults to None
        :type uid: str, optional
        :param first: first, defaults to None
        :type first: int, optional
        :param last: last, defaults to None
        :type last: int, optional
        :param after: after, defaults to None
        :type after: str, optional
        :param before: before, defaults to None
        :type before: str, optional
        :param order_field: Field to order envelopes by, defaults to None
        :type order_field: EnvelopeOrderField, optional
        :param ascending: Whether to order envelopes in ascending order, defaults to None
        :type ascending: bool, optional
        :param include_trash: Whether to include envelopes in the trash, defaults to None
        :type include_trash: bool, optional
        """
        if name is not None:
            self.name = name
        if tags is not None:
            self.tags = tags
        if comment is not None:
            self.comment = comment
        if ids is not None:
            self.ids = ids
        if statuses is not None:
            self.statuses = self._define_list(statuses, EnvelopeStatus)
        if folder_ids is not None:
            self.folder_ids = folder_ids
        if only_root_folder is not None:
            self.only_root_folder = only_root_folder
        if date_from is not None:
            self.date_from = date_from
        if date_to is not None:
            self.date_to = date_to
        if uid is not None:
            self.uid = uid
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
                order_field, EnvelopeOrderField.list(), "order_field"
            )
        if ascending is not None:
            self.ascending = ascending
        if include_trash is not None:
            self.include_trash = include_trash
        self._kwargs = kwargs
