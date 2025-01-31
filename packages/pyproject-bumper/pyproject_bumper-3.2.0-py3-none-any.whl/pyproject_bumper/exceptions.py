class PyProjectBumperError(Exception):
    """Excepción base para todos los errores del bumper."""

    pass


class InvalidVersionError(PyProjectBumperError):
    """Se lanza cuando la versión en `pyproject.toml` no coincide con el formato configurado."""

    def __init__(self, current_version, expected_format):
        message = (
            f"[ERROR]  The current version '{current_version}' is not valid for the format '{expected_format}'. "
            "Correct the version in pyproject.toml or change the format in the configuration."
        )
        super().__init__(message)


class ConfigurationError(PyProjectBumperError):
    """Se lanza cuando hay un problema en la configuración del bumper."""

    def __init__(self, message="Error in the configuration of pyproject.toml"):
        super().__init__(f"[ERROR] {message}")
