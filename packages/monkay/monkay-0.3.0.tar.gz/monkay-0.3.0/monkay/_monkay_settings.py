from __future__ import annotations

from collections.abc import Callable, Generator
from contextlib import contextmanager
from contextvars import ContextVar
from functools import cached_property
from inspect import isclass
from typing import Generic, cast

from .base import UnsetError, load
from .types import SETTINGS


class MonkaySettings(Generic[SETTINGS]):
    package: str | None
    _settings_evaluated: bool = False
    settings_preloads_name: str
    settings_extensions_name: str
    _settings_var: ContextVar[tuple[SETTINGS, list[bool]] | None] | None = None
    _settings_definition: SETTINGS | type[SETTINGS] | str | Callable[[], SETTINGS] | None = None

    @cached_property
    def _loaded_settings(self) -> SETTINGS | None:
        # only class and string pathes
        if isclass(self._settings_definition):
            return self._settings_definition()
        assert isinstance(
            self._settings_definition, str
        ), f"Not a settings object: {self._settings_definition}"
        if not self._settings_definition:
            return None
        settings: SETTINGS | type[SETTINGS] = load(self._settings_definition, package=self.package)
        if isclass(settings):
            settings = settings()
        return cast(SETTINGS, settings)

    @property
    def settings_evaluated(self) -> bool:
        assert self._settings_var is not None, "Monkay not enabled for settings"
        _settings_var = self._settings_var.get()
        if _settings_var is None:
            return self._settings_evaluated
        else:
            return _settings_var[1][0]

    @settings_evaluated.setter
    def settings_evaluated(self, value: bool) -> None:
        assert self._settings_var is not None, "Monkay not enabled for settings"
        _settings_var = self._settings_var.get()
        if _settings_var is None:
            self._settings_evaluated = value
        else:
            _settings_var[1][0] = value

    @property
    def settings(self) -> SETTINGS:
        assert self._settings_var is not None, "Monkay not enabled for settings"
        _settings_var = self._settings_var.get()
        if _settings_var is not None:
            settings: SETTINGS | Callable[[], SETTINGS] | None = _settings_var[0]
        else:
            settings = None
        if settings is None:
            # when settings_path is callable bypass the cache, for forwards
            settings = (
                self._loaded_settings
                if isinstance(self._settings_definition, str) or isclass(self._settings_definition)
                else self._settings_definition
            )
        if callable(settings):
            settings = settings()
        if settings is None:
            raise UnsetError("Settings are not set yet or the settings function returned None.")
        return settings

    @settings.setter
    def settings(
        self, value: str | Callable[[], SETTINGS] | SETTINGS | type[SETTINGS] | None
    ) -> None:
        assert self._settings_var is not None, "Monkay not enabled for settings"
        self._settings_evaluated = False
        if value is False or value is None or value == "":
            self._settings_definition = ""
            del self.settings
            return
        if not isinstance(value, str) and not callable(value) and not isclass(value):
            self._settings_definition = lambda: value
        else:
            self._settings_definition = value
        del self.settings

    @settings.deleter
    def settings(self) -> None:
        # clear cache
        self.__dict__.pop("_loaded_settings", None)

    @contextmanager
    def with_settings(self, settings: SETTINGS | None) -> Generator[SETTINGS | None]:
        assert self._settings_var is not None, "Monkay not enabled for settings"
        # why None, for temporary using the real settings
        token = self._settings_var.set((settings, [False]) if settings is not None else None)
        try:
            yield settings
        finally:
            self._settings_var.reset(token)
