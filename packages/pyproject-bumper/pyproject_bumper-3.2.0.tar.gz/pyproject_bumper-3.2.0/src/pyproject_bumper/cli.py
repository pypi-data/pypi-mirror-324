import argparse
from pathlib import Path
from .models import VersionType
from .bumper import PyProjectBumper
from .exceptions import PyProjectBumperError, InvalidVersionError


def main():
    parser = argparse.ArgumentParser(
        description="Increase the version in pyproject.toml"
    )

    parser.add_argument(
        "--type",
        type=str,
        choices=["major", "minor", "patch"],
        help="Type of version increment (only necessary for semver)",
    )

    parser.add_argument(
        "--file",
        type=str,
        default="pyproject.toml",
        help="Path to pyproject.toml file",
    )

    args = parser.parse_args()
    file_path = Path(args.file)

    if not file_path.exists():
        print(f"[ERROR] File not found {file_path}")
        return

    try:
        bumper = PyProjectBumper(file_path)
        format_type = bumper.formatter.format_type

        if format_type == "semver":
            if not args.type:
                print(
                    "[ERROR] You must specify --type for semantic versioning (major, minor, patch)"
                )
                return
            try:
                version_type = VersionType(args.type)
            except ValueError:
                print(f"[ERROR] Unrecognised versioning type: {args.type}")
                return
        else:
            version_type = VersionType(format_type)

        old_version = bumper.data["project"]["version"]
        new_version = bumper.bump(version_type)

        print(f"✅ Updated version: {old_version} → {new_version}")

    except InvalidVersionError as e:
        print(e)
    except PyProjectBumperError as e:
        print(e)
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
