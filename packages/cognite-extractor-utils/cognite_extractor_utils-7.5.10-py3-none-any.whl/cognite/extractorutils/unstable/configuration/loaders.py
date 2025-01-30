import json
from enum import Enum
from io import StringIO
from pathlib import Path
from typing import TextIO, TypeVar

from pydantic import ValidationError

from cognite.client import CogniteClient
from cognite.extractorutils.configtools.loaders import _load_yaml_dict_raw
from cognite.extractorutils.exceptions import InvalidConfigError as OldInvalidConfigError
from cognite.extractorutils.unstable.configuration.exceptions import InvalidConfigError
from cognite.extractorutils.unstable.configuration.models import ConfigModel

__all__ = ["ConfigFormat", "load_file", "load_from_cdf", "load_io", "load_dict"]


_T = TypeVar("_T", bound=ConfigModel)


class ConfigFormat(Enum):
    JSON = "json"
    YAML = "yaml"


def load_file(path: Path, schema: type[_T]) -> _T:
    if path.suffix in [".yaml", ".yml"]:
        format = ConfigFormat.YAML
    elif path.suffix == ".json":
        format = ConfigFormat.JSON
    else:
        raise InvalidConfigError(f"Unknown file type {path.suffix}")

    with open(path) as stream:
        return load_io(stream, format, schema)


def load_from_cdf(
    cognite_client: CogniteClient, external_id: str, schema: type[_T], revision: int | None = None
) -> tuple[_T, int]:
    params: dict[str, str | int] = {"integration": external_id}
    if revision:
        params["revision"] = revision
    response = cognite_client.get(
        f"/api/v1/projects/{cognite_client.config.project}/odin/config",
        params=params,
        headers={"cdf-version": "alpha"},
    )
    response.raise_for_status()
    data = response.json()

    try:
        return load_io(StringIO(data["config"]), ConfigFormat.YAML, schema), data["revision"]

    except InvalidConfigError as e:
        e.attempted_revision = data["revision"]
        raise e
    except OldInvalidConfigError as e:
        new_e = InvalidConfigError(e.message)
        new_e.attempted_revision = data["revision"]
        raise new_e from e


def load_io(stream: TextIO, format: ConfigFormat, schema: type[_T]) -> _T:
    if format == ConfigFormat.JSON:
        data = json.load(stream)

    elif format == ConfigFormat.YAML:
        data = _load_yaml_dict_raw(stream)

        if "azure-keyvault" in data:
            data.pop("azure-keyvault")
        if "key-vault" in data:
            data.pop("key-vault")

    return load_dict(data, schema)


def _make_loc_str(loc: tuple) -> str:
    # Remove the body parameter if it is present
    if loc[0] == "body":
        loc = loc[1:]

    # Create a string from the loc parameter
    loc_str = ""
    needs_sep = False
    for lo in loc:
        if not needs_sep:
            loc_str = f"{loc_str}{lo}"
            needs_sep = True
        else:
            if isinstance(lo, int):
                loc_str = f"{loc_str}[{lo}]"
            else:
                loc_str = f"{loc_str}.{lo}"

    return loc_str


def load_dict(data: dict, schema: type[_T]) -> _T:
    try:
        return schema.model_validate(data)

    except ValidationError as e:
        messages = []
        for err in e.errors():
            loc = err.get("loc")
            if loc is None:
                continue

            # Create a string from the loc parameter
            loc_str = _make_loc_str(loc)

            if "ctx" in err and "error" in err["ctx"]:
                exc = err["ctx"]["error"]
                if isinstance(exc, ValueError) or isinstance(exc, AssertionError):
                    messages.append(f"{str(exc)}: {loc_str}")
                    continue

            messages.append(f"{err.get('msg')}: {loc_str}")

        raise InvalidConfigError(", ".join(messages), details=messages) from e
