import dataclasses
from typing import Any, Callable

from fastapi_authix.exceptions import UnknownObject, InvalidMode
from fastapi_authix.typing import SerializeMode


class Inspect:
    def __init__(self, obj: Any) -> None:
        self._object = obj

    def is_dict(self) -> bool:
        return isinstance(self._object, dict)

    def is_dataclass(self) -> bool:
        return dataclasses.is_dataclass(self._object) and not isinstance(self._object, type)

    def is_pydantic_model(self) -> bool:
        return hasattr(self._object, "__fields__") and hasattr(self._object, "schema")

    def is_sqlalchemy_model(self) -> bool:
        return hasattr(self._object, "__table__")


class Serializer:
    def __init__(self, obj: Any, *, mode: SerializeMode = "auto") -> None:
        self._object = obj
        self._mode = self._detect_mode() if mode == "auto" else mode
        self._method = self._choose_serializer()

    def _detect_mode(self) -> SerializeMode:
        inspect = Inspect(self._object)

        if inspect.is_dict():
            return "dict"
        elif inspect.is_dataclass():
            return "dataclass"
        elif inspect.is_pydantic_model():
            return "pydantic"
        elif inspect.is_sqlalchemy_model():
            return "sqlalchemy"
        else:
            raise UnknownObject()

    def _choose_serializer(self) -> Callable[[], dict[str, Any]]:
        match self._mode:
            case "dict":
                return self._serialize_dict
            case "dataclass":
                return self._serialize_dataclass
            case "pydantic":
                return self._serialize_pydantic
            case "sqlalchemy":
                return self._serialize_sqlalchemy
            case _:
                raise InvalidMode(self._mode)

    def _serialize_dict(self) -> dict[str, Any]:
        return self._object

    def _serialize_dataclass(self) -> dict[str, Any]:
        return dataclasses.asdict(self._object)

    def _serialize_pydantic(self) -> dict[str, Any]:
        return self._object.model_dump(mode="json")

    def _serialize_sqlalchemy(self) -> dict[str, Any]:
        from sqlalchemy.inspection import inspect
        return {c.key: getattr(self._object, c.key) for c in inspect(self._object).mapper.column_attrs}

    def serialize(self) -> dict[str, Any]:
        return self._method()

    def deserialize(self, payload: dict[str, Any]) -> Any:
        return self._object.__class__(**payload)
