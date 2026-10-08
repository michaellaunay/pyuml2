"""Reject runtime imports that escape the locally qualified package roots."""
from pathlib import Path
import sys


def pytest_sessionstart(session):
    import pyecore, pyuml2, pyecoregen, multigen
    session._runtime_roots = {
        m.__name__: Path(m.__file__).resolve().parent
        for m in (pyecore, pyuml2, pyecoregen, multigen)
    }


def pytest_sessionfinish(session, exitstatus):
    for name, module in list(sys.modules.items()):
        root = session._runtime_roots.get(name.split('.')[0])
        if root is not None and getattr(module, '__file__', None):
            assert Path(module.__file__).resolve().is_relative_to(root), (name, module.__file__)
