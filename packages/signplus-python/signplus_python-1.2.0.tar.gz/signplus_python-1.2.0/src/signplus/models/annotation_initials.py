from .utils.json_map import JsonMap
from .utils.base_model import BaseModel


@JsonMap({"id_": "id"})
class AnnotationInitials(BaseModel):
    """Initials annotation (null if annotation is not initials)

    :param id_: Unique identifier of the annotation initials, defaults to None
    :type id_: str, optional
    """

    def __init__(self, id_: str = None, **kwargs):
        """Initials annotation (null if annotation is not initials)

        :param id_: Unique identifier of the annotation initials, defaults to None
        :type id_: str, optional
        """
        if id_ is not None:
            self.id_ = id_
        self._kwargs = kwargs
