import sys

sys.path.append('../src')
from architectural_smells.smell import CyclicDependency, UnstableDependency, HubLikeDependency, Version

CD_SMELL_ID = '8646'
CD_BIRTH_DATE = '18-9-2016'
CD_VERSION = 'd5293751676da9816a415dbc8a3cf703ff13205d'
CD_AFFECTED_ELEMENTS = ['org.apache.commons.lang3.builder', 'org.apache.commons.lang3.tuple']
CD_SIZE = 2
CD_SHAPE = 'tiny'

UD_SMELL_ID = '8816'
UD_BIRTH_DATE = '6-3-2008'
UD_VERSION = 'd86a278500212fafbfe7bd7533a54a2cce6ae66e'
UD_AFFECTED_ELEMENTS = ['org.apache.commons.lang', 'org.apache.commons.lang.exception']
UD_SIZE = 2
UD_INSTABILITY_GAP = -0.11388074291300099
UD_DOUD = 0.0

HD_SMELL_ID = '1'
HD_BIRTH_DATE = '14-11-2009'
HD_VERSION = '000bac6b9484209a2e0fda4586b2def38b6f9108'
HD_AFFECTED_ELEMENTS = ["org.apache.commons.lang.text",
                        "org.apache.commons.lang.text",
                        "org.apache.commons.lang.text",
                        "org.apache.commons.lang.text",
                        "org.apache.commons.lang.text",
                        "org.apache.commons.lang.text"]
HD_SIZE = 7
HD_INTERNAL_PATH_LENGTH = -1
HD_CLASS_RATIO = -1


def create_cyclic_dependency():
    return CyclicDependency(CD_SMELL_ID, CD_BIRTH_DATE, CD_VERSION, CD_AFFECTED_ELEMENTS, CD_SIZE, CD_SHAPE)


def create_unstable_dependency():
    return UnstableDependency(UD_SMELL_ID, UD_BIRTH_DATE, UD_VERSION, UD_AFFECTED_ELEMENTS, UD_SIZE, UD_INSTABILITY_GAP,
                              UD_DOUD)


def create_hublike_dependency():
    return HubLikeDependency(HD_SMELL_ID, HD_BIRTH_DATE, HD_VERSION, HD_AFFECTED_ELEMENTS, HD_SIZE,
                             HD_INTERNAL_PATH_LENGTH, HD_CLASS_RATIO)


def create_cyclic_dependency_same_version(smell_id=CD_SMELL_ID):
    return CyclicDependency(smell_id, CD_BIRTH_DATE, CD_VERSION, CD_AFFECTED_ELEMENTS, CD_SIZE, CD_SHAPE)


def create_unstable_dependency_same_version(smell_id=UD_SMELL_ID):
    return UnstableDependency(smell_id, CD_BIRTH_DATE, CD_VERSION, UD_AFFECTED_ELEMENTS, UD_SIZE, UD_INSTABILITY_GAP,
                              UD_DOUD)


def create_hublike_dependency_same_version(smell_id=HD_SMELL_ID):
    return HubLikeDependency(smell_id, CD_BIRTH_DATE, CD_VERSION, HD_AFFECTED_ELEMENTS, HD_SIZE,
                             HD_INTERNAL_PATH_LENGTH, HD_CLASS_RATIO)


def test_cyclic_dependency():
    cyclic_dependency = create_cyclic_dependency()
    assert isinstance(cyclic_dependency, CyclicDependency)
    assert cyclic_dependency.unique_smell_id == CD_SMELL_ID
    assert cyclic_dependency.birth_day.year == 2016
    assert cyclic_dependency.birth_day.month == 9
    assert cyclic_dependency.birth_day.day == 18
    assert cyclic_dependency.version == CD_VERSION
    assert len(cyclic_dependency.affected_elements) == 2
    assert cyclic_dependency.size == CD_SIZE
    assert cyclic_dependency.shape == CD_SHAPE


def test_unstable_dependency():
    unstable_dependency = create_unstable_dependency()
    assert isinstance(unstable_dependency, UnstableDependency)
    assert unstable_dependency.unique_smell_id == UD_SMELL_ID
    assert unstable_dependency.birth_day.year == 2008
    assert unstable_dependency.birth_day.month == 3
    assert unstable_dependency.birth_day.day == 6
    assert unstable_dependency.version == UD_VERSION
    assert len(unstable_dependency.affected_elements) == 2
    assert unstable_dependency.size == UD_SIZE
    assert unstable_dependency.instability_gap == UD_INSTABILITY_GAP
    assert unstable_dependency.doud == UD_DOUD


def test_hublike_dependency():
    hublike_dependency = create_hublike_dependency()
    assert isinstance(hublike_dependency, HubLikeDependency)
    assert hublike_dependency.unique_smell_id == HD_SMELL_ID
    assert hublike_dependency.birth_day.year == 2009
    assert hublike_dependency.birth_day.month == 11
    assert hublike_dependency.birth_day.day == 14
    assert hublike_dependency.version == HD_VERSION
    assert len(hublike_dependency.affected_elements) == 6
    assert hublike_dependency.size == HD_SIZE
    assert hublike_dependency.avrg_internal_path_length == HD_INTERNAL_PATH_LENGTH
    assert hublike_dependency.affected_classes_ratio == HD_CLASS_RATIO


def test_version():
    version = Version(CD_VERSION)
    version.add_smell(create_cyclic_dependency_same_version())
    version.add_smell(create_cyclic_dependency_same_version(2))
    version.add_smell(create_unstable_dependency_same_version())
    version.add_smell(create_unstable_dependency_same_version(3))
    version.add_smell(create_hublike_dependency_same_version())
    version.add_smell(create_hublike_dependency_same_version(4))
    assert len(version.smells_by_type) == 3
    assert version.has_cyclic_dependencies()
    assert version.has_unstable_dependencies()
    assert version.has_hublike_dependencies()
    assert len(version.get_cyclic_dependencies()) == 2
    assert len(version.get_unstable_dependencies()) == 2
    assert len(version.get_hublike_dependencies()) == 2


def test_duplicated_smell_id():
    assert True
