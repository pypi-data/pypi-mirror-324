from enum import Enum


class VersionType(Enum):
    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"
    DATE = "date"
    BUILD = "build"
    INC = "inc"
