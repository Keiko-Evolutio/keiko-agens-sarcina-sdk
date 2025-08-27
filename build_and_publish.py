#!/usr/bin/env python3
"""
Build und Publish Script für KEI-Agent Python SDK.

Dieses Script automatisiert den Build- und Veröffentlichungsprozess
für das KEI-Agent Python SDK.
"""

import argparse
import glob
from pathlib import Path
import shutil
import subprocess
import sys


def run_command(cmd: list, description: str) -> bool:
    """Führt einen Befehl aus und gibt den Erfolg zurück."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ {description} erfolgreich")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} fehlgeschlagen (Exit Code: {e.returncode})")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False
    except Exception as e:
        print(f"⚠️ {description} Fehler: {e}")
        return False


def clean_build():
    """Räumt Build-Artefakte auf."""
    print("🧹 Räume Build-Artefakte auf...")

    # Verzeichnisse zum Löschen
    dirs_to_clean = [
        "build",
        "dist",
        "*.egg-info",
        "htmlcov",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
    ]

    for pattern in dirs_to_clean:
        if "*" in pattern:
            # Glob pattern
            for path in glob.glob(pattern):
                if Path(path).exists():
                    if Path(path).is_dir():
                        shutil.rmtree(path)
                        print(f"  Entfernt: {path}/")
                    else:
                        Path(path).unlink()
                        print(f"  Entfernt: {path}")
        else:
            # Direkter Pfad
            path = Path(pattern)
            if path.exists():
                if path.is_dir():
                    import shutil

                    shutil.rmtree(path)
                    print(f"  Entfernt: {path}/")
                else:
                    path.unlink()
                    print(f"  Entfernt: {path}")

    print("✅ Build-Artefakte aufgeräumt")


def build_package():
    """Erstellt das Package."""
    print("🏗️ Erstelle Package...")

    # Installiere build falls nicht vorhanden
    if not run_command(
        [sys.executable, "-m", "pip", "install", "build"], "Build-Tool Installation"
    ):
        return False

    # Erstelle Source Distribution und Wheel
    if not run_command([sys.executable, "-m", "build"], "Package Build"):
        return False

    # Prüfe ob Artefakte erstellt wurden
    dist_dir = Path("dist")
    if not dist_dir.exists():
        print("❌ Dist-Verzeichnis nicht gefunden")
        return False

    files = list(dist_dir.glob("*"))
    if not files:
        print("❌ Keine Build-Artefakte gefunden")
        return False

    print("✅ Build-Artefakte erstellt:")
    for file in files:
        print(f"  - {file.name}")

    return True


def check_package():
    """Prüft das erstellte Package."""
    print("🔍 Prüfe Package...")

    # Installiere twine falls nicht vorhanden
    if not run_command([sys.executable, "-m", "pip", "install", "twine"], "Twine Installation"):
        return False

    # Prüfe Package mit twine
    if not run_command([sys.executable, "-m", "twine", "check", "dist/*"], "Package Check"):
        print("⚠️ Twine Check fehlgeschlagen, aber Build kann fortgesetzt werden")

    return True


def publish_test():
    """Veröffentlicht auf TestPyPI."""
    print("📤 Veröffentliche auf TestPyPI...")

    cmd = [sys.executable, "-m", "twine", "upload", "--repository", "testpypi", "dist/*"]

    return run_command(cmd, "TestPyPI Upload")


def publish_prod():
    """Veröffentlicht auf PyPI."""
    print("📤 Veröffentliche auf PyPI...")

    # Sicherheitsabfrage
    response = input("⚠️ Wirklich auf PyPI veröffentlichen? (yes/no): ")
    if response.lower() != "yes":
        print("❌ Veröffentlichung abgebrochen")
        return False

    cmd = [sys.executable, "-m", "twine", "upload", "dist/*"]

    return run_command(cmd, "PyPI Upload")


def main():
    """Hauptfunktion."""
    parser = argparse.ArgumentParser(description="KEI-Agent SDK Build und Publish")
    parser.add_argument(
        "--build-only", action="store_true", help="Nur Build, keine Veröffentlichung"
    )
    parser.add_argument("--publish-test", action="store_true", help="Veröffentliche auf TestPyPI")
    parser.add_argument("--publish-prod", action="store_true", help="Veröffentliche auf PyPI")
    parser.add_argument("--no-clean", action="store_true", help="Überspringe Cleanup")

    args = parser.parse_args()

    print("🚀 KEI-Agent SDK Build und Publish")
    print("=" * 50)

    success = True

    # Cleanup
    if not args.no_clean:
        clean_build()

    # Build
    if not build_package():
        success = False

    # Check
    if success and not check_package():
        print("⚠️ Package Check fehlgeschlagen, aber Build war erfolgreich")

    # Publish
    if success and args.publish_test:
        success = publish_test()
    elif success and args.publish_prod:
        success = publish_prod()

    print("=" * 50)
    if success:
        if args.build_only:
            print("✅ Build erfolgreich abgeschlossen!")
        elif args.publish_test:
            print("✅ TestPyPI Veröffentlichung erfolgreich!")
        elif args.publish_prod:
            print("✅ PyPI Veröffentlichung erfolgreich!")
        else:
            print("✅ Build erfolgreich abgeschlossen!")
        sys.exit(0)
    else:
        print("❌ Prozess fehlgeschlagen!")
        sys.exit(1)


if __name__ == "__main__":
    main()
