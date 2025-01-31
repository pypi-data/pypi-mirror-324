from pathlib import Path

import tomli
import tomli_w

from .exceptions import InvalidVersionError
from .formatters import VersionFormatter
from .models import VersionType


class PyProjectBumper:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.data = self._read_pyproject()
        self.config = self.data.get("tool", {}).get("pyproject-bumper", {})
        self.formatter = VersionFormatter(self.config)

    def _read_pyproject(self) -> dict:
        """Lee el archivo pyproject.toml."""
        with open(self.file_path, "rb") as f:
            return tomli.load(f)

    def _write_pyproject(self):
        """Escribe el archivo pyproject.toml."""
        with open(self.file_path, "wb") as f:
            tomli_w.dump(self.data, f)

    def _is_version_valid(self, current_version: str) -> bool:
        """
        Verifica si la versión actual coincide con el formato especificado en la configuración.
        """
        format_type = self.formatter.format_type

        if format_type == "semver":
            parts = current_version.split(".")
            return len(parts) == 3 and all(p.isdigit() for p in parts)

        elif format_type == "date":
            parts = current_version.split(".")
            return len(parts) >= 3 and parts[0].isdigit() and len(parts[0]) == 4

        elif format_type == "build":
            parts = current_version.split(".")
            return len(parts) >= 3 and all(p.isdigit() for p in parts[:3])

        elif format_type == "inc":
            return current_version.isdigit()

        return False  # Si el tipo es desconocido

    def bump(self, version_type: VersionType) -> str:
        """Incrementa la versión según el tipo especificado."""
        current_version = self.data["project"]["version"]

        if version_type not in VersionType.__members__.values():
            raise KeyError(f"Version type not supported: {version_type}")

        if self.formatter.format_type == "semver" and version_type not in [
            VersionType.MAJOR,
            VersionType.MINOR,
            VersionType.PATCH,
        ]:
            raise KeyError(
                f"Version type not supported: {version_type} for semver format"
            )

        if not self._is_version_valid(current_version):
            raise InvalidVersionError(current_version, self.formatter.format_type)

        new_version = self.formatter.bump_version(current_version, version_type)
        self.data["project"]["version"] = new_version
        self._write_pyproject()
        return new_version
