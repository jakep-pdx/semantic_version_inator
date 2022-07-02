import pytest
from semantic_version_inator import next_semantic_version


test_base_file_name = "ap_ado_utils-1.1.1-py3-none-any.whl"
test_patch_ver = "1.1.2"
test_minor_ver = "1.2.0"
test_major_ver = "2.0.0"


def test_get_next_version_given_file_name_patch():
    """ call get_next_version_given_file_name given base name and patch release type """
    new_ver = next_semantic_version.get_next_version_given_file_name(test_base_file_name, "PATCH")
    assert new_ver == test_patch_ver


def test_get_next_version_given_file_name_minor():
    """ call get_next_version_given_file_name given base name and mior release type """
    new_ver = next_semantic_version.get_next_version_given_file_name(test_base_file_name, "MINOR")
    assert new_ver == test_minor_ver


def test_get_next_version_given_file_name_major():
    """ call get_next_version_given_file_name given base name and major release type """
    new_ver = next_semantic_version.get_next_version_given_file_name(test_base_file_name, "MAJOR")
    assert new_ver == test_major_ver


def test_get_next_version_given_file_name_bad_file():
    """ call get_next_version_given_file_name with a bad file name, should throw ValueError """
    with pytest.raises(ValueError):
        next_semantic_version.get_next_version_given_file_name("badfilename", "MAJOR")


def test_get_next_version_given_file_name_bad_version():
    """ call get_next_version_given_file_name with a bad version num, should throw ValueError """
    with pytest.raises(ValueError):
        next_semantic_version.get_next_version_given_file_name("bad-x.x.x-version-number", "MAJOR")


def test_get_next_version_given_file_name_bad_release_type():
    """ call get_next_version_given_file_name with a bad release type, should throw ValueError """
    with pytest.raises(ValueError):
        next_semantic_version.get_next_version_given_file_name(test_base_file_name, "XYZ")
