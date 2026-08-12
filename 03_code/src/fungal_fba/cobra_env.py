"""Environment shims that must run *before* ``import cobra``.

Two host-specific problems are handled here:

1. cobrapy instantiates a ``Configuration`` singleton at import time, which
   probes a per-user cache directory. In a sandboxed workspace that path is
   not writable and the import dies with ``PermissionError``.
2. Reading real-world SBML emits thousands of libSBML warning lines on stderr
   (unsupported ``layout``/``render`` packages, non-conforming MIRIAM URNs).
   Left alone this floods any log or notebook.

Usage — always call :func:`prepare` first::

    from fungal_fba.cobra_env import prepare, quiet_read_sbml
    prepare()
    import cobra
"""

from __future__ import annotations

import contextlib
import io
import logging
import os
import pathlib
import warnings

_PREPARED = False


def prepare(cache_dir: str | os.PathLike = "cobra_cache") -> pathlib.Path:
    """Point cobrapy's cache at a writable directory and silence SBML noise.

    Must be called before ``import cobra``. Idempotent.

    Returns the absolute cache path that was configured.
    """
    global _PREPARED
    cache = pathlib.Path(cache_dir).absolute()
    cache.mkdir(parents=True, exist_ok=True)

    # cobrapy resolves its cache under XDG_CACHE_HOME (or HOME on macOS), and
    # appdirs consults HOME directly, so both are redirected into the workspace.
    os.environ["XDG_CACHE_HOME"] = str(cache)
    os.environ.setdefault("COBRAPY_CACHE_DIRECTORY", str(cache))
    os.environ["HOME"] = str(pathlib.Path(".").absolute())

    warnings.filterwarnings("ignore")
    for name in ("cobra", "cobra.io.sbml", "libsbml"):
        logging.getLogger(name).setLevel(logging.ERROR)

    _PREPARED = True
    return cache


def quiet_read_sbml(path: str | os.PathLike):
    """Read an SBML model with stderr suppressed.

    cobrapy routes libSBML diagnostics to stderr rather than the logging
    module, so redirecting the stream is the only way to keep output readable.
    """
    if not _PREPARED:
        prepare()
    import cobra  # imported lazily so prepare() always runs first

    buf = io.StringIO()
    with contextlib.redirect_stderr(buf):
        model = cobra.io.read_sbml_model(str(path))
    return model


def quiet_load(path: str | os.PathLike):
    """Load a model from SBML (.xml/.sbml) or JSON (.json), quietly.

    Mirrors ``labUtils.fba.fba_tools.load_model`` but suppresses the SBML
    warning flood and tolerates ``.json``.
    """
    if not _PREPARED:
        prepare()
    import cobra

    p = str(path)
    if p.endswith((".xml", ".sbml")):
        return quiet_read_sbml(p)
    if p.endswith(".json"):
        buf = io.StringIO()
        with contextlib.redirect_stderr(buf):
            return cobra.io.load_json_model(p)
    raise ValueError(f"Unsupported model format: {p}")
