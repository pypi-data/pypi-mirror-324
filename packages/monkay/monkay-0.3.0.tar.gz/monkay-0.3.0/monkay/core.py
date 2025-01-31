from __future__ import annotations

import warnings
from collections.abc import Callable, Iterable
from contextvars import ContextVar
from importlib import import_module
from typing import (
    Any,
    Generic,
    Literal,
)

from ._monkay_exports import MonkayExports
from ._monkay_instance import MonkayInstance
from ._monkay_settings import MonkaySettings
from .base import UnsetError, evaluate_preloads, get_value_from_settings
from .types import (
    INSTANCE,
    PRE_ADD_LAZY_IMPORT_HOOK,
    SETTINGS,
    DeprecatedImport,
    ExtensionProtocol,
)


class Monkay(
    MonkayInstance[INSTANCE, SETTINGS],
    MonkaySettings[SETTINGS],
    MonkayExports,
    Generic[INSTANCE, SETTINGS],
):
    def __init__(
        self,
        globals_dict: dict,
        *,
        with_instance: str | bool = False,
        with_extensions: str | bool = False,
        extension_order_key_fn: None
        | Callable[[ExtensionProtocol[INSTANCE, SETTINGS]], Any] = None,
        settings_path: str
        | Callable[[], SETTINGS]
        | SETTINGS
        | type[SETTINGS]
        | Literal[False]
        | None = None,
        preloads: Iterable[str] = (),
        settings_preloads_name: str = "",
        settings_extensions_name: str = "",
        uncached_imports: Iterable[str] = (),
        lazy_imports: dict[str, str | Callable[[], Any]] | None = None,
        deprecated_lazy_imports: dict[str, DeprecatedImport] | None = None,
        settings_ctx_name: str = "monkay_settings_ctx",
        extensions_applied_ctx_name: str = "monkay_extensions_applied_ctx",
        skip_all_update: bool = False,
        skip_getattr_fixup: bool = False,
        evaluate_settings: None = None,
        ignore_settings_import_errors: bool = True,
        pre_add_lazy_import_hook: None | PRE_ADD_LAZY_IMPORT_HOOK = None,
        post_add_lazy_import_hook: None | Callable[[str], None] = None,
        ignore_preload_import_errors: bool = True,
        package: str | None = "",
    ) -> None:
        self.globals_dict = globals_dict
        if with_instance is True:
            with_instance = "monkay_instance_ctx"
        with_instance = with_instance
        if with_extensions is True:
            with_extensions = "monkay_extensions_ctx"
        with_extensions = with_extensions
        if package == "" and globals_dict.get("__spec__"):
            package = globals_dict["__spec__"].parent
        self.package = package or None

        self._cached_imports: dict[str, Any] = {}
        self.pre_add_lazy_import_hook = pre_add_lazy_import_hook
        self.post_add_lazy_import_hook = post_add_lazy_import_hook
        self.uncached_imports = set(uncached_imports)
        self.lazy_imports = {}
        self.deprecated_lazy_imports = {}
        if lazy_imports:
            for name, lazy_import in lazy_imports.items():
                self.add_lazy_import(name, lazy_import, no_hooks=True)
        if deprecated_lazy_imports:
            for name, deprecated_import in deprecated_lazy_imports.items():
                self.add_deprecated_lazy_import(name, deprecated_import, no_hooks=True)
        if settings_path is not None and settings_path is not False:
            self._settings_var = globals_dict[settings_ctx_name] = ContextVar(
                settings_ctx_name, default=None
            )
            self.settings = settings_path  # type: ignore
        self.settings_preloads_name = settings_preloads_name
        self.settings_extensions_name = settings_extensions_name

        if with_instance:
            self._instance_var = globals_dict[with_instance] = ContextVar(
                with_instance, default=None
            )
        if with_extensions:
            self.extension_order_key_fn = extension_order_key_fn
            self._extensions = {}
            self._extensions_var = globals_dict[with_extensions] = ContextVar(
                with_extensions, default=None
            )
            self._extensions_applied_var = globals_dict[extensions_applied_ctx_name] = ContextVar(
                extensions_applied_ctx_name, default=None
            )
        if not skip_all_update and (self.lazy_imports or self.deprecated_lazy_imports):
            all_var = globals_dict.setdefault("__all__", [])
            globals_dict["__all__"] = self.update_all_var(all_var)
        # fix missing __dir__ in case only __getattr__ was specified and __dir__ not
        # it assumes the __all__ var is correct
        if (
            not skip_getattr_fixup
            and "__all__" in globals_dict
            and "__getattr__" in globals_dict
            and "__dir__" not in globals_dict
        ):
            self._init_global_dir_hook()
        self.evaluate_preloads(preloads, ignore_import_errors=ignore_preload_import_errors)
        if evaluate_settings is not None:
            raise Exception(
                "This feature and the evaluate_settings parameter are removed in monkay 0.3"
            )

    def clear_caches(self, settings_cache: bool = True, import_cache: bool = True) -> None:
        if settings_cache:
            del self.settings
        if import_cache:
            self._cached_imports.clear()

    def evaluate_preloads(
        self,
        preloads: Iterable[str],
        *,
        ignore_import_errors: bool = True,
        package: str | None = None,
    ) -> bool:
        return evaluate_preloads(
            preloads, ignore_import_errors=ignore_import_errors, package=package or self.package
        )
        no_errors: bool = True
        for preload in preloads:
            splitted = preload.rsplit(":", 1)
            try:
                module = import_module(splitted[0], self.package)
            except (ImportError, AttributeError) as exc:
                if not ignore_import_errors:
                    raise exc
                no_errors = False
                continue
            if len(splitted) == 2:
                getattr(module, splitted[1])()
        return no_errors

    def _evaluate_settings(
        self,
        *,
        settings: SETTINGS,
        on_conflict: Literal["error", "keep", "replace"],
        ignore_preload_import_errors: bool,
        initial_settings_evaluated: bool,
    ) -> None:
        self.settings_evaluated = True

        try:
            if self.settings_preloads_name:
                settings_preloads = get_value_from_settings(settings, self.settings_preloads_name)
                self.evaluate_preloads(
                    settings_preloads, ignore_import_errors=ignore_preload_import_errors
                )
            if self.settings_extensions_name:
                for extension in get_value_from_settings(settings, self.settings_extensions_name):
                    self.add_extension(extension, use_overwrite=True, on_conflict=on_conflict)
        except Exception as exc:
            if not initial_settings_evaluated:
                self.settings_evaluated = False
            raise exc

    def evaluate_settings(
        self,
        *,
        on_conflict: Literal["error", "keep", "replace"] = "error",
        ignore_import_errors: bool = False,
        ignore_preload_import_errors: bool = True,
        onetime: bool = True,
    ) -> bool:
        initial_settings_evaluated = self.settings_evaluated
        if onetime and initial_settings_evaluated:
            return True
        # don't access settings when there is nothing to evaluate
        if not self.settings_preloads_name and not self.settings_extensions_name:
            self.settings_evaluated = True
            return True

        try:
            # load settings one time and before setting settings_evaluated to True
            settings = self.settings
        except Exception as exc:
            if ignore_import_errors and isinstance(exc, (UnsetError, ImportError, AttributeError)):
                return False
            raise exc
        self._evaluate_settings(
            on_conflict=on_conflict,
            settings=settings,
            ignore_preload_import_errors=ignore_preload_import_errors,
            initial_settings_evaluated=initial_settings_evaluated,
        )
        return True

    def evaluate_settings_once(
        self,
        *,
        on_conflict: Literal["error", "keep", "replace"] = "error",
        ignore_import_errors: bool = True,
    ) -> bool:
        warnings.warn(
            "`evaluate_settings_once` is deprecated. Use `evaluate_settings` instead. It has now the same functionality.",
            stacklevel=2,
        )
        return self.evaluate_settings(
            on_conflict=on_conflict, ignore_import_errors=ignore_import_errors, onetime=True
        )
