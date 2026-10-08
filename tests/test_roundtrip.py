from pathlib import Path

import pytest
from pyecore.ecore import EProxy
from pyecore.resources import ResourceSet
from pyecore.resources.json import JsonResource
import pyuml2.uml as uml


def resources():
    rset = ResourceSet()
    rset.metamodel_registry[uml.nsURI] = uml
    rset.resource_factory['json'] = JsonResource
    return rset


def resolved(value):
    return value.force_resolve() if isinstance(value, EProxy) else value


def check_model(model):
    base, child, association, profile = model.packagedElement
    assert base.name == 'Base'
    assert list(child.superClass) == [base]
    assert resolved(child.generalization[0].general) is base
    assert resolved(child.ownedAttribute[0].type) is base
    assert child.ownedAttribute[0].owner is child
    assert [resolved(p) for p in association.memberEnd] == list(association.ownedEnd)
    assert resolved(association.ownedEnd[0].type) is base
    assert resolved(association.ownedEnd[1].type) is child
    assert isinstance(profile, uml.Profile)
    assert isinstance(profile.packagedElement[0], uml.Stereotype)
    assert child.qualifiedName == model.name + '::Child'
    assert child in model.all_owned_elements()


@pytest.mark.parametrize('extension', ['uml', 'json'])
def test_corpus_load_modify_save_reload(tmp_path, extension):
    original = Path(__file__).with_name('corpus') / 'packages.uml'
    model = resources().get_resource(str(original)).contents[0]
    check_model(model)
    model.name = 'Modifié_Δ'
    model.packagedElement[1].ownedAttribute[0].name = 'référence'
    output = tmp_path / ('modèle.' + extension)
    resource = resources().create_resource(str(output))
    resource.append(model)
    resource.save()
    reloaded = resources().get_resource(str(output)).contents[0]
    check_model(reloaded)
    assert reloaded.name == 'Modifié_Δ'
    assert reloaded.packagedElement[1].ownedAttribute[0].name == 'référence'


def test_profile_operations_remain_explicitly_unimplemented():
    package, profile, stereotype = uml.Package(), uml.Profile(), uml.Stereotype()
    for operation in (lambda: package.apply_profile(profile), profile.define,
                      lambda: package.apply_stereotype(stereotype)):
        with pytest.raises(NotImplementedError):
            operation()
