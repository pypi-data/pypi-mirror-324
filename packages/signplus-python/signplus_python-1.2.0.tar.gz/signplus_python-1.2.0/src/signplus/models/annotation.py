from __future__ import annotations
from .utils.json_map import JsonMap
from .utils.base_model import BaseModel
from .annotation_type import AnnotationType
from .annotation_signature import AnnotationSignature
from .annotation_initials import AnnotationInitials
from .annotation_text import AnnotationText
from .annotation_date_time import AnnotationDateTime
from .annotation_checkbox import AnnotationCheckbox


@JsonMap({"id_": "id", "type_": "type", "datetime_": "datetime"})
class Annotation(BaseModel):
    """Annotation

    :param id_: Unique identifier of the annotation, defaults to None
    :type id_: str, optional
    :param recipient_id: ID of the recipient, defaults to None
    :type recipient_id: str, optional
    :param document_id: ID of the document, defaults to None
    :type document_id: str, optional
    :param page: Page number where the annotation is placed, defaults to None
    :type page: int, optional
    :param x: X coordinate of the annotation (in % of the page width from 0 to 100) from the top left corner, defaults to None
    :type x: float, optional
    :param y: Y coordinate of the annotation (in % of the page height from 0 to 100) from the top left corner, defaults to None
    :type y: float, optional
    :param width: Width of the annotation (in % of the page width from 0 to 100), defaults to None
    :type width: float, optional
    :param height: Height of the annotation (in % of the page height from 0 to 100), defaults to None
    :type height: float, optional
    :param required: Whether the annotation is required, defaults to None
    :type required: bool, optional
    :param type_: Type of the annotation, defaults to None
    :type type_: AnnotationType, optional
    :param signature: Signature annotation (null if annotation is not a signature), defaults to None
    :type signature: AnnotationSignature, optional
    :param initials: Initials annotation (null if annotation is not initials), defaults to None
    :type initials: AnnotationInitials, optional
    :param text: Text annotation (null if annotation is not a text), defaults to None
    :type text: AnnotationText, optional
    :param datetime_: Date annotation (null if annotation is not a date), defaults to None
    :type datetime_: AnnotationDateTime, optional
    :param checkbox: Checkbox annotation (null if annotation is not a checkbox), defaults to None
    :type checkbox: AnnotationCheckbox, optional
    """

    def __init__(
        self,
        id_: str = None,
        recipient_id: str = None,
        document_id: str = None,
        page: int = None,
        x: float = None,
        y: float = None,
        width: float = None,
        height: float = None,
        required: bool = None,
        type_: AnnotationType = None,
        signature: AnnotationSignature = None,
        initials: AnnotationInitials = None,
        text: AnnotationText = None,
        datetime_: AnnotationDateTime = None,
        checkbox: AnnotationCheckbox = None,
        **kwargs,
    ):
        """Annotation

        :param id_: Unique identifier of the annotation, defaults to None
        :type id_: str, optional
        :param recipient_id: ID of the recipient, defaults to None
        :type recipient_id: str, optional
        :param document_id: ID of the document, defaults to None
        :type document_id: str, optional
        :param page: Page number where the annotation is placed, defaults to None
        :type page: int, optional
        :param x: X coordinate of the annotation (in % of the page width from 0 to 100) from the top left corner, defaults to None
        :type x: float, optional
        :param y: Y coordinate of the annotation (in % of the page height from 0 to 100) from the top left corner, defaults to None
        :type y: float, optional
        :param width: Width of the annotation (in % of the page width from 0 to 100), defaults to None
        :type width: float, optional
        :param height: Height of the annotation (in % of the page height from 0 to 100), defaults to None
        :type height: float, optional
        :param required: Whether the annotation is required, defaults to None
        :type required: bool, optional
        :param type_: Type of the annotation, defaults to None
        :type type_: AnnotationType, optional
        :param signature: Signature annotation (null if annotation is not a signature), defaults to None
        :type signature: AnnotationSignature, optional
        :param initials: Initials annotation (null if annotation is not initials), defaults to None
        :type initials: AnnotationInitials, optional
        :param text: Text annotation (null if annotation is not a text), defaults to None
        :type text: AnnotationText, optional
        :param datetime_: Date annotation (null if annotation is not a date), defaults to None
        :type datetime_: AnnotationDateTime, optional
        :param checkbox: Checkbox annotation (null if annotation is not a checkbox), defaults to None
        :type checkbox: AnnotationCheckbox, optional
        """
        if id_ is not None:
            self.id_ = id_
        if recipient_id is not None:
            self.recipient_id = recipient_id
        if document_id is not None:
            self.document_id = document_id
        if page is not None:
            self.page = page
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
        if required is not None:
            self.required = required
        if type_ is not None:
            self.type_ = self._enum_matching(type_, AnnotationType.list(), "type_")
        if signature is not None:
            self.signature = self._define_object(signature, AnnotationSignature)
        if initials is not None:
            self.initials = self._define_object(initials, AnnotationInitials)
        if text is not None:
            self.text = self._define_object(text, AnnotationText)
        if datetime_ is not None:
            self.datetime_ = self._define_object(datetime_, AnnotationDateTime)
        if checkbox is not None:
            self.checkbox = self._define_object(checkbox, AnnotationCheckbox)
        self._kwargs = kwargs
