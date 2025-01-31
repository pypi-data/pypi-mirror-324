from datetime import datetime
from typing import Any, Dict, Optional

from .models import VersionType


class VersionFormatter:
    """Maneja diferentes formatos de versiones basados en la configuración."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.format_type = self.config.get("version_format", "semver")

    def bump_version(self, current_version: str, version_type: VersionType) -> str:
        """Incrementa la versión según el formato configurado."""
        type_functions = {
            "date": self._bump_date,
            "build": self._bump_build,
            "inc": self._bump_incremental,
        }
        if version_type not in VersionType.__members__.values():
            raise KeyError(f"Version type not supported: {version_type}")

        if self.format_type not in type_functions.keys():
            raise ValueError(f"Version format not supported: {self.format_type}")

        if self.format_type == "semver":
            return self._bump_semver(current_version, version_type)

        return type_functions[self.format_type](current_version)

    def _bump_semver(self, current_version: str, version_type: VersionType) -> str:
        """Incrementa versión en formato semántico (MAJOR.MINOR.PATCH)."""
        major, minor, patch = map(int, current_version.split("."))

        if version_type == VersionType.MAJOR:
            return f"{major + 1}.0.0"
        elif version_type == VersionType.MINOR:
            return f"{major}.{minor + 1}.0"
        else:  # PATCH
            return f"{major}.{minor}.{patch + 1}"

    def _bump_date(self, current_version: str) -> str:
        """Incrementa versión en formato de fecha (YYYY.MM.DD.BUILD)."""
        date_format = self.config.get("date_format", "%Y.%m.%d")
        current_date = datetime.now().strftime(date_format)

        if "." not in current_version:
            build = 1
        else:
            *_, build_str = current_version.split(".")
            try:
                build = int(build_str) + 1
            except ValueError:
                build = 1

        return f"{current_date}.{build}"

    def _bump_build(self, current_version: str) -> str:
        """Incrementa el número de build (X.Y.Z.BUILD)."""
        parts = current_version.split(".")
        if len(parts) < 4:
            parts.append("0")
        parts[-1] = str(int(parts[-1]) + 1)
        return ".".join(parts)

    def _bump_incremental(self, current_version: str) -> str:
        """Incrementa una versión numérica (Rolling Release)."""
        return str(int(current_version) + 1)
