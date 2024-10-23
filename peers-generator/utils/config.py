import os
import tomllib

from datetime import date
from typing import Any


class TomlConfig(object):
    def __init__(self, path: str) -> None:
        self.path = path
        self._config: dict[str, Any] = {}
        self.administrators_ids: list[int] = []


    def load(self):
        if not os.path.exists(os.path.join(self.path, "config.toml")):
            self._config = {"ADMIN": {"ADMINISTRATORS_IDS": self.administrators_ids}}
            return
        with open(os.path.join(self.path, "config.toml"), "rb") as f:
            self._config = tomllib.load(f)
            self.administrators_ids = self._config["ADMIN"]["ADMINISTRATORS_IDS"]

    def dumps(self, toml_dict: dict = None, table: str = "") -> str:
        if toml_dict is None:
            toml_dict = self._config
        document = []
        for key, value in toml_dict.items():
            match value:
                case dict():
                    table_key = f"{table}.{key}" if table else key
                    document.append(
                        f"\n[{table_key}]\n{self.dumps(value, table=table_key)}"
                    )
                case _:
                    document.append(f"{key} = {self._dumps_value(value)}")
        return "\n".join(document)

    def _dumps_value(self, value):
        match value:
            case bool():
                return "true" if value else "false"
            case float() | int():
                return str(value)
            case str():
                return f'"{value}"'
            case date():
                return value.isoformat()
            case list():
                return f"[{', '.join(self._dumps_value(v) for v in value)}]"
            case _:
                raise TypeError(
                    f"{type(value).__name__} {value!r} is not supported"
                )


class BotConfig(object):
    def __init__(self, path: str) -> None:
        self.path = path
        self._config: TomlConfig = ...
        self.administrators_ids: list[int] = []

    def __enter__(self):
        self._config = TomlConfig(self.path)
        self._config.load()
        self.administrators_ids = self._config.administrators_ids
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with open(os.path.join(self.path, "config.toml"), "+w") as config_file:
            config_file.write(self._config.dumps())

    def __repr__(self):
        return "BotConfig(path={})".format(self.path)

if __name__ == "__main__":
    conf = BotConfig(path="./config.toml")
    with conf:
        print(conf)
    # breakpoint()
