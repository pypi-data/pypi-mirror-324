import os
from typing import Any, TypeVar

import pydantic

from liblaf import grapes

_C = TypeVar("_C", bound=pydantic.BaseModel)


def load_pydantic(
    fpath: str | os.PathLike[str], cls: type[_C], *, ext: str | None = None
) -> _C:
    data: Any = grapes.deserialize(fpath, ext=ext)
    return cls.model_validate(data)


def save_pydantic(
    fpath: str | os.PathLike[str],
    data: pydantic.BaseModel,
    *,
    ext: str | None = None,
    # pydantic.BaseModel.model_dump(**kwargs)
    context: Any | None = None,
    by_alias: bool = False,
    exclude_unset: bool = False,
    exclude_defaults: bool = False,
    exclude_none: bool = False,
    round_trip: bool = False,
    serialize_as_any: bool = False,
) -> None:
    grapes.serialize(
        fpath,
        data.model_dump(
            context=context,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            serialize_as_any=serialize_as_any,
        ),
        ext=ext,
    )
