import pathlib
import uuid
from django.utils.text import slugify


def airplane_image_path(instance, filename) -> pathlib.Path:
    filename = (
        f"{slugify(instance.name)}-{uuid.uuid4()}"
        + pathlib.Path(filename).suffix
    )
    return pathlib.Path("upload/airplanes/") / pathlib.Path(filename)
