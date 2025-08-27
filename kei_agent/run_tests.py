#!/usr/bin/env python3
"""
Zentraler Test-Runner für KEI-Agent Python SDK.

Dieser Test-Runner orchestriert verschiedene Test-Kategorien und bietet
eine einheitliche Schnittstelle für lokale Entwicklung und CI/CD.
"""

import argparse
import os
from pathlib import Path
import subprocess
import sys
from typing import List, Optional


def run_command(cmd: List[str], description: str, timeout: int = 300) -> bool:
    """Führt einen Befehl aus und gibt den Erfolg zurück."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=timeout)
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
    except subprocess.TimeoutExpired:
        print(f"⏰ {description} Timeout nach {timeout}s")
        return False
    except Exception as e:
        print(f"⚠️ {description} Fehler: {e}")
        return False


def get_pytest_base_cmd(coverage: bool = True) -> List[str]:
    """Erstellt den Basis-pytest Befehl."""
    cmd = [sys.executable, "-m", "pytest"]

    if coverage:
        cmd.extend(
            [
                "--cov=kei_agent",
                "--cov-report=xml",
                "--cov-report=html:htmlcov",
                "--cov-report=term-missing",
                "--cov-branch",
            ]
        )

    return cmd


def run_unit_tests(verbose: bool = False, coverage: bool = True) -> bool:
    """Führt Unit Tests aus."""
    cmd = get_pytest_base_cmd(coverage)
    cmd.extend(["-m", "unit"])

    if verbose:
        cmd.append("-v")

    # Spezifische Test-Dateien für Unit Tests
    test_files = [
        "tests/test_import_system.py",
        "tests/test_config.py",
        "tests/test_core_functionality.py",
        "tests/test_utils_edge_cases.py",
        "tests/test_exception_handling_security.py",
        "tests/test_input_validation.py",
        "tests/test_metrics.py",
        "tests/test_retry_edge_cases.py",
    ]

    # Nur existierende Dateien hinzufügen
    existing_files = [f for f in test_files if Path(f).exists()]
    if existing_files:
        cmd.extend(existing_files)
    else:
        # Fallback: alle Tests im tests/ Verzeichnis
        cmd.append("tests/")

    return run_command(cmd, "Unit Tests")


def run_integration_tests(verbose: bool = False, coverage: bool = True) -> bool:
    """Führt Integration Tests aus."""
    # Setze Umgebungsvariable für Integration Tests
    env = os.environ.copy()
    env["RUN_INTEGRATION_TESTS"] = "1"

    cmd = get_pytest_base_cmd(coverage)
    cmd.extend(["-m", "integration"])

    if verbose:
        cmd.append("-v")

    # Integration Test Verzeichnisse
    test_paths = [
        "tests/integration/",
        "tests/test_unified_client_integration.py",
        "tests/test_config_management.py",
    ]

    existing_paths = [p for p in test_paths if Path(p).exists()]
    if existing_paths:
        cmd.extend(existing_paths)

    print("🔄 Integration Tests...")
    try:
        result = subprocess.run(
            cmd, check=True, capture_output=True, text=True, timeout=300, env=env
        )
        print("✅ Integration Tests erfolgreich")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Integration Tests fehlgeschlagen (Exit Code: {e.returncode})")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False
    except Exception as e:
        print(f"⚠️ Integration Tests Fehler: {e}")
        return False


def run_protocol_tests(protocol: Optional[str] = None, verbose: bool = False) -> bool:
    """Führt Protocol Tests aus."""
    cmd = get_pytest_base_cmd(coverage=False)  # Protocol Tests ohne Coverage
    cmd.extend(["-m", "protocol"])

    if verbose:
        cmd.append("-v")

    # Protocol-spezifische Tests
    test_files = [
        "tests/test_protocol_clients.py",
        "tests/test_protocol_clients_extended.py",
        "tests/test_protocol_selector.py",
        "tests/test_protocol_types.py",
        "tests/test_protocol_retry_policies.py",
    ]

    existing_files = [f for f in test_files if Path(f).exists()]
    if existing_files:
        cmd.extend(existing_files)

    description = f"Protocol Tests ({protocol})" if protocol else "Protocol Tests"
    return run_command(cmd, description)


def run_security_tests(verbose: bool = False) -> bool:
    """Führt Security Tests aus."""
    cmd = get_pytest_base_cmd(coverage=False)
    cmd.extend(["-m", "security"])

    if verbose:
        cmd.append("-v")

    # Security-spezifische Tests
    test_files = [
        "tests/test_security_manager.py",
        "tests/test_security_manager_extended.py",
        "tests/test_security_manager_httpx.py",
        "tests/test_secrets_management.py",
        "tests/test_dependency_security.py",
    ]

    existing_files = [f for f in test_files if Path(f).exists()]
    if existing_files:
        cmd.extend(existing_files)

    return run_command(cmd, "Security Tests")


def run_performance_tests(verbose: bool = False) -> bool:
    """Führt Performance Tests aus."""
    cmd = get_pytest_base_cmd(coverage=False)
    cmd.extend(["-m", "performance"])

    if verbose:
        cmd.append("-v")

    # Performance Test Verzeichnis
    if Path("tests/performance/").exists():
        cmd.append("tests/performance/")

    return run_command(cmd, "Performance Tests", timeout=600)  # Längerer Timeout


def run_refactored_tests(verbose: bool = False) -> bool:
    """Führt Tests für refactored Komponenten aus."""
    cmd = get_pytest_base_cmd(coverage=True)

    if verbose:
        cmd.append("-v")

    # Refactored Component Tests
    test_files = [
        "tests/test_unified_client_refactored.py",
        "tests/test_enterprise_logging_unit.py",
        "tests/test_operational_dashboards.py",
        "tests/test_error_aggregation.py",
    ]

    existing_files = [f for f in test_files if Path(f).exists()]
    if existing_files:
        cmd.extend(existing_files)
    else:
        print("⚠️ Keine refactored Tests gefunden")
        return True

    return run_command(cmd, "Refactored Component Tests")


def main() -> None:
    """Hauptfunktion des Test-Runners."""
    parser = argparse.ArgumentParser(description="KEI-Agent SDK Test Runner")
    parser.add_argument("--unit", action="store_true", help="Führe Unit Tests aus")
    parser.add_argument("--integration", action="store_true", help="Führe Integration Tests aus")
    parser.add_argument("--protocol", nargs="?", const="all", help="Führe Protocol Tests aus")
    parser.add_argument("--security", action="store_true", help="Führe Security Tests aus")
    parser.add_argument("--performance", action="store_true", help="Führe Performance Tests aus")
    parser.add_argument("--refactored", action="store_true", help="Führe Refactored Tests aus")
    parser.add_argument("--all", action="store_true", help="Führe alle Tests aus")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose Output")
    parser.add_argument("--no-coverage", action="store_true", help="Deaktiviere Coverage")

    args = parser.parse_args()

    # Wenn keine spezifischen Tests angegeben, führe Unit Tests aus
    if not any(
        [
            args.unit,
            args.integration,
            args.protocol,
            args.security,
            args.performance,
            args.refactored,
            args.all,
        ]
    ):
        args.unit = True

    coverage = not args.no_coverage
    success = True

    print("🚀 KEI-Agent SDK Test Runner")
    print("=" * 50)

    if args.all or args.unit:
        success &= run_unit_tests(args.verbose, coverage)

    if args.all or args.integration:
        success &= run_integration_tests(args.verbose, coverage)

    if args.all or args.protocol:
        success &= run_protocol_tests(
            args.protocol if args.protocol != "all" else None, args.verbose
        )

    if args.all or args.security:
        success &= run_security_tests(args.verbose)

    if args.all or args.performance:
        success &= run_performance_tests(args.verbose)

    if args.all or args.refactored:
        success &= run_refactored_tests(args.verbose)

    print("=" * 50)
    if success:
        print("✅ Alle Tests erfolgreich abgeschlossen!")
        sys.exit(0)
    else:
        print("❌ Einige Tests sind fehlgeschlagen!")
        sys.exit(1)


if __name__ == "__main__":
    main()
