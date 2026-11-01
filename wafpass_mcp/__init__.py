"""Deprecated compatibility package — import :mod:`wombat_mcp` instead."""

from __future__ import annotations

import importlib
import importlib.abc
import importlib.util
import sys
import warnings

warnings.warn(
    "The 'wafpass_mcp' package is deprecated after the WAF++ → Wombat "
    "rebrand; import 'wombat_mcp' instead.",
    DeprecationWarning,
    stacklevel=2,
)


class _WombatAliasLoader(importlib.abc.Loader):
    def create_module(self, spec):  # noqa: ANN001 - importlib protocol
        return None

    def exec_module(self, module) -> None:  # noqa: ANN001 - importlib protocol
        target_name = "wombat_mcp" + module.__name__[len("wafpass_mcp"):]
        target = importlib.import_module(target_name)
        module.__dict__.update(target.__dict__)
        module.__doc__ = target.__doc__


class _WombatAliasFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):  # noqa: ANN001
        if fullname.startswith("wafpass_mcp."):
            return importlib.util.spec_from_loader(fullname, _WombatAliasLoader())
        return None


sys.meta_path.insert(0, _WombatAliasFinder())
