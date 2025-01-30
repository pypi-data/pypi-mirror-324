from __future__ import annotations
from .utils.json_map import JsonMap
from .utils.base_model import BaseModel
from .annotation_checkbox_style import AnnotationCheckboxStyle


@JsonMap({})
class AnnotationCheckbox(BaseModel):
    """Checkbox annotation (null if annotation is not a checkbox)

    :param checked: Whether the checkbox is checked, defaults to None
    :type checked: bool, optional
    :param style: Style of the checkbox, defaults to None
    :type style: AnnotationCheckboxStyle, optional
    """

    def __init__(
        self, checked: bool = None, style: AnnotationCheckboxStyle = None, **kwargs
    ):
        """Checkbox annotation (null if annotation is not a checkbox)

        :param checked: Whether the checkbox is checked, defaults to None
        :type checked: bool, optional
        :param style: Style of the checkbox, defaults to None
        :type style: AnnotationCheckboxStyle, optional
        """
        if checked is not None:
            self.checked = checked
        if style is not None:
            self.style = self._enum_matching(
                style, AnnotationCheckboxStyle.list(), "style"
            )
        self._kwargs = kwargs
