"""Reproducible candidate generation, separate from the handwritten runtime.

The output is a candidate for review, not an automatic replacement for pyuml2.
Install the generation extra and use the locally qualified ecosystem forks.
"""
from contextlib import contextmanager
from pathlib import Path
import re
import sysconfig

import pyecore.ecore as ecore
from pyecore.resources import ResourceSet


def to_snake_case(name):
    first = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', first).lower()


@contextmanager
def snake_pythonic_names():
    from pyecoregen.adapter import fix_name_clash
    original = ecore.ENamedElement.__getattribute__

    def get_attribute(self, name):
        value = original(self, name)
        if name == 'name':
            value = fix_name_clash(value)
            if isinstance(self, ecore.EOperation):
                value = to_snake_case(value)
        return value

    ecore.ENamedElement.__getattribute__ = get_attribute
    try:
        yield
    finally:
        ecore.ENamedElement.__getattribute__ = original


def setup_resourceset():
    import pyuml2.types as types
    rset = ResourceSet()
    rset.metamodel_registry['platform:/plugin/org.eclipse.uml2.types/model/Types.ecore'] = types
    rset.metamodel_registry['platform:/plugin/org.eclipse.emf.ecore/model/Ecore.ecore'] = ecore
    return rset


def model_path():
    source = Path(__file__).resolve().parents[1] / 'model' / 'uml.ecore'
    if source.is_file():
        return source
    return Path(sysconfig.get_path('data')) / 'share/pyuml2/model/uml.ecore'


def generate_code(output, *, model=None):
    """Generate a review candidate into an explicit output directory.

    The existing runtime, including custom type converters and manual mixins,
    must be preserved when reviewing/integrating this candidate.
    """
    import pyecoregen.ecore as generator_module
    root = setup_resourceset().get_resource(str(model or model_path())).contents[0]
    class UMLGenerator(generator_module.EcoreGenerator):
        module_path_map = {**generator_module.EcoreGenerator.module_path_map,
                           'types': 'pyuml2.types'}

        @staticmethod
        def filter_all_contents(value, type_):
            # UML duplicates annotations contain descriptive EReferences that
            # are not structural features. They must not become assignments.
            return (item for item in value.eAllContents()
                    if isinstance(item, type_)
                    and not (isinstance(item, ecore.EReference)
                             and item.eContainingClass is None))

    generator = UMLGenerator(user_module='pyuml2.uml_mixins')
    original = generator_module.pythonic_names
    generator_module.pythonic_names = snake_pythonic_names
    try:
        generator.generate(root, str(output))
    finally:
        generator_module.pythonic_names = original


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, help='Separate candidate output directory')
    parser.add_argument('--model', type=Path)
    args = parser.parse_args()
    generate_code(args.output, model=args.model)


if __name__ == '__main__':
    main()
