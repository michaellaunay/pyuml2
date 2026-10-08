import hashlib
import subprocess
import sys
from pathlib import Path

import pytest
import pyecore.ecore as ecore
import pyecoregen.ecore as generator_module

from pyuml2 import generation


def test_names_restored_after_error():
    original = ecore.ENamedElement.__getattribute__
    adapter = generator_module.pythonic_names
    with pytest.raises(RuntimeError):
        with generation.snake_pythonic_names():
            assert ecore.EOperation('hasOwner').name == 'has_owner'
            raise RuntimeError('formatter failure')
    assert ecore.ENamedElement.__getattribute__ is original
    assert generator_module.pythonic_names is adapter


def test_generation_separate_and_deterministic(tmp_path):
    model = Path(__file__).resolve().parents[1] / 'model' / 'uml.ecore'
    before = hashlib.sha256(model.read_bytes()).hexdigest()
    for folder in ('first', 'second'):
        generation.generate_code(tmp_path / folder, model=model)
    def files(folder):
        return {str(p.relative_to(folder)): p.read_bytes()
                for p in folder.rglob('*') if p.is_file()}
    first = files(tmp_path / 'first')
    assert first == files(tmp_path / 'second')
    assert 'uml/uml.py' in first
    compile(first['uml/uml.py'], 'generated/uml.py', 'exec')
    assert hashlib.sha256(model.read_bytes()).hexdigest() == before

    script = """
import sys
import pyuml2
pyuml2.__path__.insert(0, sys.argv[1])
import pyuml2.uml as uml
assert uml.nsURI == 'http://www.eclipse.org/uml2/5.0.0/UML'
p = uml.Package(name='P')
b = uml.Class(name='Base')
c = uml.Class(name='Child')
p.packagedElement.extend([b, c])
c.superClass.append(b)
c.ownedAttribute.append(uml.Property(name='attribute', type=b))
assert list(c.superClass) == [b]
assert c.qualifiedName == 'P::Child'
assert c.ownedAttribute[0].owner is c
"""
    subprocess.run([sys.executable, '-c', script, str(tmp_path / 'first')], check=True)
