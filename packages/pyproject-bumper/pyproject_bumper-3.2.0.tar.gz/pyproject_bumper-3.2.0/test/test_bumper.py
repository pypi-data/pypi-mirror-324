import pytest
import tomli_w
from pathlib import Path
from datetime import datetime
from pyproject_bumper.bumper import PyProjectBumper
from pyproject_bumper.models import VersionType
from pyproject_bumper.exceptions import InvalidVersionError


@pytest.fixture
def tmp_pyproject(tmp_path):
    """Crea un archivo pyproject.toml temporal para pruebas."""
    file_path = tmp_path / "pyproject.toml"
    return file_path


@pytest.fixture
def semver_pyproject(tmp_pyproject):
    """Configura un pyproject.toml con formato SemVer."""
    config = {
        "tool": {"pyproject-bumper": {"version_format": "semver"}},
        "project": {"version": "1.2.3"},
    }
    with open(tmp_pyproject, "wb") as f:
        tomli_w.dump(config, f)
    return tmp_pyproject


@pytest.fixture
def date_pyproject(tmp_pyproject):
    """Configura un pyproject.toml con formato Date."""
    today = datetime.now().strftime("%Y.%m.%d")
    config = {
        "tool": {"pyproject-bumper": {"version_format": "date"}},
        "project": {"version": f"{today}.2"},
    }
    with open(tmp_pyproject, "wb") as f:
        tomli_w.dump(config, f)
    return tmp_pyproject


### TESTS PARA SEMVER ###


def test_bump_major(semver_pyproject):
    bumper = PyProjectBumper(semver_pyproject)
    new_version = bumper.bump(VersionType.MAJOR)
    assert new_version == "2.0.0"


def test_bump_minor(semver_pyproject):
    bumper = PyProjectBumper(semver_pyproject)
    new_version = bumper.bump(VersionType.MINOR)
    assert new_version == "1.3.0"


def test_bump_patch(semver_pyproject):
    bumper = PyProjectBumper(semver_pyproject)
    new_version = bumper.bump(VersionType.PATCH)
    assert new_version == "1.2.4"


### TESTS PARA DATE VERSIONING ###


def test_bump_date(date_pyproject):
    bumper = PyProjectBumper(date_pyproject)
    new_version = bumper.bump(VersionType.DATE)
    today = datetime.now().strftime("%Y.%m.%d")
    assert new_version.startswith(f"{today}.")  # Incrementa el build number


### TESTS PARA ERRORES ###


def test_invalid_version_format(tmp_pyproject):
    """Prueba que lanzar un bump en un formato incorrecto genera un error."""
    config = {
        "tool": {"pyproject-bumper": {"version_format": "semver"}},
        "project": {"version": "2025.01.29.4"},  # Formato incorrecto
    }
    with open(tmp_pyproject, "wb") as f:
        tomli_w.dump(config, f)

    bumper = PyProjectBumper(tmp_pyproject)
    with pytest.raises(InvalidVersionError):
        bumper.bump(VersionType.MAJOR)


def test_missing_pyproject():
    """Prueba que si no existe el archivo pyproject.toml, el bumper lanza un error."""
    file_path = Path("fake_pyproject.toml")
    with pytest.raises(FileNotFoundError):
        PyProjectBumper(file_path)


def test_invalid_type_for_semver(semver_pyproject):
    """Prueba que no se puede hacer bump sin --type en semver."""
    bumper = PyProjectBumper(semver_pyproject)
    with pytest.raises(KeyError):
        bumper.bump(VersionType.DATE)  # No debería estar permitido
