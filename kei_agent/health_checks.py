# sdk/python/kei_agent/health_checks.py
"""
Enterprise Health Checks for KEI-Agent SDK.

Implementiert aroatdfassende Health-Check-Mechatismen for monitoring,
Alerting and automatische Wietheherstellung in Production-Aroatdgebungen.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
import asyncio
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
import time
from typing import Any, Dict, List, Optional

from .enterprise_logging import get_logger

# Initializes Module-Logr
_logger = get_logger(__name__)


class HealthStatus(str, Enum):
    """Health Status-Werte für Komponenten.

    Attributes:
        HEALTHY: Komponente funktioniert normal
        DEGRADED: Komponente funktioniert mit Einschränkungen
        UNHEALTHY: Komponente funktioniert nicht
        UNKNOWN: Status kann nicht ermittelt werden
    """

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


@dataclass
class HealthCheckResult:
    """result of a Health-Checks.

    Attributes:
        name: Name the gechecksen Komponente
        status: health status
        message: Beschreibung of the status
        details: Tosätzliche Details and Metrics
        timestamp: Zeitpunkt the Prüfung
        duration_ms: Dauer the Prüfung in Millisekatthe
        error: error-information on Problemen
    """

    name: str
    status: HealthStatus
    message: str
    details: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    duration_ms: Optional[float] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Konvertiert Health-Check-Result to dictionary.

        Returns:
            dictionary-Repräsentation of the Results
        """
        return {
            "name": self.name,
            "status": self.status.value,
            "message": self.message,
            "details": self.details,
            "timestamp": self.timestamp.isoformat(),
            "duration_ms": self.duration_ms,
            "error": self.error,
        }


class BaseHealthCheck(ABC):
    """Abstrakte Basisklasse for Health-Checks.

    Definiert Interface for all Health-Check-Implementierungen
    with gemasamen functionalitäten wie Timeout and retry-Logik.
    """

    def __init__(
        self,
        name: str,
        timeout_seconds: float = 5.0,
        critical: bool = True,
        tags: Optional[List[str]] = None,
    ) -> None:
        """Initializes Base Health Check.

        Args:
            name: Name the Komponente
            timeout_seconds: Timeout for Health-Check
            critical: Ob Check kritisch for Gesamtstatus is
            tags: Tags for Kategorisierung
        """
        self.name = name
        self.timeout_seconds = timeout_seconds
        self.critical = critical
        self.tags = tags or []

    @abstractmethod
    async def check(self) -> HealthCheckResult:
        """Executes Health-Check out.

        Returns:
            Health-Check-Result
        """

    async def run_check(self) -> HealthCheckResult:
        """Executes Health-Check with Timeout and Error-Hatdling out.

        Returns:
            Health-Check-Result with Timing-informationen
        """
        start_time = time.time()

        try:
            # Führe Check with Timeout out
            result = await asyncio.wait_for(self.check(), timeout=self.timeout_seconds)

            # Füge Timing-information hinto
            duration_ms = (time.time() - start_time) * 1000
            result.duration_ms = duration_ms

            return result

        except asyncio.TimeoutError:
            duration_ms = (time.time() - start_time) * 1000
            return HealthCheckResult(
                name=self.name,
                status=HealthStatus.UNHEALTHY,
                message=f"Health-Check Timeout after {self.timeout_seconds}s",
                duration_ms=duration_ms,
                error="timeout",
            )
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            return HealthCheckResult(
                name=self.name,
                status=HealthStatus.UNHEALTHY,
                message=f"Health-Check error: {e!s}",
                duration_ms=duration_ms,
                error=str(e),
            )


class DatabaseHealthCheck(BaseHealthCheck):
    """Health-Check for databatkverbindungen."""

    def __init__(
        self,
        name: str = "database",
        connection_string: Optional[str] = None,
        query: str = "SELECT 1",
        **kwargs: Any,
    ) -> None:
        """Initializes Database Health Check.

        Args:
            name: Name of the Checks
            connection_string: databatk-connectionsstring
            query: Test-Query for connectionsprüfung
            **kwargs: Tosätzliche parameters for BaseHealthCheck
        """
        super().__init__(name, **kwargs)
        self.connection_string = connection_string
        self.query = query

    async def check(self) -> HealthCheckResult:
        """Checks databatkverbindung."""
        if not self.connection_string:
            return HealthCheckResult(
                name=self.name,
                status=HealthStatus.UNKNOWN,
                message="Keine Datenbankverbindung konfiguriert",
            )

        try:
            # Implementiere echte Datenbankverbindung basierend auf Connection String
            result = await self._test_database_connection()

            return HealthCheckResult(
                name=self.name,
                status=result["status"],
                message=result["message"],
                details=result["details"],
            )
        except Exception as e:
            return HealthCheckResult(
                name=self.name,
                status=HealthStatus.UNHEALTHY,
                message=f"Datenbankverbindung fehlgeschlagen: {e!s}",
                error=str(e),
            )

    async def _test_database_connection(self) -> Dict[str, Any]:
        """Testet echte Datenbankverbindung basierend auf Connection String.

        Returns:
            Dictionary mit Status, Message und Details der Verbindung
        """
        if not self.connection_string:
            return {
                "status": HealthStatus.UNKNOWN,
                "message": "Keine Datenbankverbindung konfiguriert",
                "details": {},
            }

        # Erkenne Datenbanktyp aus Connection String
        db_type = self._detect_database_type(self.connection_string)

        try:
            if db_type == "postgresql":
                return await self._test_postgresql_connection()
            if db_type == "mysql":
                return await self._test_mysql_connection()
            if db_type == "sqlite":
                return await self._test_sqlite_connection()
            # Fallback: Generischer Test
            return await self._test_generic_connection()

        except ImportError as e:
            return {
                "status": HealthStatus.DEGRADED,
                "message": f"Datenbank-Driver nicht installiert: {e!s}",
                "details": {
                    "database_type": db_type,
                    "required_package": self._get_required_package(db_type),
                    "install_command": f"pip install {self._get_required_package(db_type)}",
                },
            }
        except Exception as e:
            return {
                "status": HealthStatus.UNHEALTHY,
                "message": f"Datenbankverbindung fehlgeschlagen: {e!s}",
                "details": {"database_type": db_type, "error": str(e)},
            }

    def _detect_database_type(self, connection_string: str) -> str:
        """Erkennt Datenbanktyp aus Connection String.

        Args:
            connection_string: Datenbank-Connection String

        Returns:
            Erkannter Datenbanktyp
        """
        connection_string = connection_string.lower()

        if connection_string.startswith(("postgresql://", "postgres://")):
            return "postgresql"
        if connection_string.startswith("mysql://"):
            return "mysql"
        if connection_string.startswith("sqlite://") or connection_string.endswith(".db"):
            return "sqlite"
        return "unknown"

    def _get_required_package(self, db_type: str) -> str:
        """Gibt erforderliches Package für Datenbanktyp zurück.

        Args:
            db_type: Datenbanktyp

        Returns:
            Name des erforderlichen Python-Packages
        """
        packages = {"postgresql": "asyncpg", "mysql": "aiomysql", "sqlite": "aiosqlite"}
        return packages.get(db_type, "unknown")

    async def _test_postgresql_connection(self) -> Dict[str, Any]:
        """Testet PostgreSQL-Verbindung.

        Returns:
            Dictionary mit Testergebnis
        """
        import asyncpg

        start_time = time.time()

        try:
            # Verbindung herstellen
            conn = await asyncpg.connect(self.connection_string)

            # Test-Query ausführen
            result = await conn.fetchval(self.query)

            # Verbindungsstatistiken abrufen
            server_version = conn.get_server_version()

            await conn.close()

            response_time = (time.time() - start_time) * 1000

            return {
                "status": HealthStatus.HEALTHY,
                "message": "PostgreSQL-Verbindung erfolgreich",
                "details": {
                    "query": self.query,
                    "query_result": result,
                    "response_time_ms": response_time,
                    "server_version": f"{server_version.major}.{server_version.minor}.{server_version.micro}",
                    "database_type": "postgresql",
                },
            }

        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            return {
                "status": HealthStatus.UNHEALTHY,
                "message": f"PostgreSQL-Verbindung fehlgeschlagen: {e!s}",
                "details": {
                    "query": self.query,
                    "response_time_ms": response_time,
                    "database_type": "postgresql",
                    "error": str(e),
                },
            }

    async def _test_mysql_connection(self) -> Dict[str, Any]:
        """Testet MySQL-Verbindung.

        Returns:
            Dictionary mit Testergebnis
        """
        import aiomysql

        start_time = time.time()

        try:
            # Connection String parsen
            # Format: mysql://user:password@host:port/database
            import urllib.parse

            parsed = urllib.parse.urlparse(self.connection_string)

            # Verbindung herstellen
            conn = await aiomysql.connect(
                host=parsed.hostname,
                port=parsed.port or 3306,
                user=parsed.username,
                password=parsed.password,
                db=parsed.path.lstrip("/") if parsed.path else None,
            )

            # Test-Query ausführen
            cursor = await conn.cursor()
            await cursor.execute(self.query)
            result = await cursor.fetchone()
            await cursor.close()

            # Server-Info abrufen
            cursor = await conn.cursor()
            await cursor.execute("SELECT VERSION()")
            server_version = await cursor.fetchone()
            await cursor.close()

            conn.close()

            response_time = (time.time() - start_time) * 1000

            return {
                "status": HealthStatus.HEALTHY,
                "message": "MySQL-Verbindung erfolgreich",
                "details": {
                    "query": self.query,
                    "query_result": result[0] if result else None,
                    "response_time_ms": response_time,
                    "server_version": server_version[0] if server_version else "unknown",
                    "database_type": "mysql",
                },
            }

        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            return {
                "status": HealthStatus.UNHEALTHY,
                "message": f"MySQL-Verbindung fehlgeschlagen: {e!s}",
                "details": {
                    "query": self.query,
                    "response_time_ms": response_time,
                    "database_type": "mysql",
                    "error": str(e),
                },
            }

    async def _test_sqlite_connection(self) -> Dict[str, Any]:
        """Testet SQLite-Verbindung.

        Returns:
            Dictionary mit Testergebnis
        """
        import aiosqlite

        start_time = time.time()

        try:
            # SQLite-Datei aus Connection String extrahieren
            db_path = self.connection_string.replace("sqlite://", "").replace("sqlite:///", "")

            # Verbindung herstellen
            async with aiosqlite.connect(db_path) as conn:
                # Test-Query ausführen
                cursor = await conn.execute(self.query)
                result = await cursor.fetchone()
                await cursor.close()

                # SQLite-Version abrufen
                cursor = await conn.execute("SELECT sqlite_version()")
                version_result = await cursor.fetchone()
                await cursor.close()

            response_time = (time.time() - start_time) * 1000

            return {
                "status": HealthStatus.HEALTHY,
                "message": "SQLite-Verbindung erfolgreich",
                "details": {
                    "query": self.query,
                    "query_result": result[0] if result else None,
                    "response_time_ms": response_time,
                    "sqlite_version": version_result[0] if version_result else "unknown",
                    "database_type": "sqlite",
                    "database_path": db_path,
                },
            }

        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            return {
                "status": HealthStatus.UNHEALTHY,
                "message": f"SQLite-Verbindung fehlgeschlagen: {e!s}",
                "details": {
                    "query": self.query,
                    "response_time_ms": response_time,
                    "database_type": "sqlite",
                    "error": str(e),
                },
            }

    async def _test_generic_connection(self) -> Dict[str, Any]:
        """Generischer Datenbankverbindungstest für unbekannte Typen.

        Returns:
            Dictionary mit Testergebnis
        """
        start_time = time.time()

        try:
            # Versuche verschiedene Standard-Bibliotheken
            connection_tested = False

            # Versuche SQLAlchemy (falls verfügbar)
            try:
                from sqlalchemy.ext.asyncio import create_async_engine

                engine = create_async_engine(self.connection_string)

                async with engine.begin() as conn:
                    result = await conn.execute(self.query)
                    query_result = result.scalar()

                await engine.dispose()
                connection_tested = True

                response_time = (time.time() - start_time) * 1000

                return {
                    "status": HealthStatus.HEALTHY,
                    "message": "Datenbankverbindung erfolgreich (SQLAlchemy)",
                    "details": {
                        "query": self.query,
                        "query_result": query_result,
                        "response_time_ms": response_time,
                        "database_type": "generic_sqlalchemy",
                        "connection_method": "sqlalchemy",
                    },
                }

            except ImportError:
                pass

            # Falls SQLAlchemy nicht verfügbar, Fallback auf Simulation mit Warnung
            if not connection_tested:
                await asyncio.sleep(0.1)  # Simuliere Verbindungszeit

                response_time = (time.time() - start_time) * 1000

                return {
                    "status": HealthStatus.DEGRADED,
                    "message": "Datenbankverbindung simuliert - kein passender Driver gefunden",
                    "details": {
                        "query": self.query,
                        "response_time_ms": response_time,
                        "database_type": "simulated",
                        "connection_method": "simulation",
                        "warning": "Installiere entsprechende Datenbank-Driver für echte Tests",
                    },
                }

        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            return {
                "status": HealthStatus.UNHEALTHY,
                "message": f"Generischer Datenbanktest fehlgeschlagen: {e!s}",
                "details": {
                    "query": self.query,
                    "response_time_ms": response_time,
                    "database_type": "generic",
                    "error": str(e),
                },
            }


class APIHealthCheck(BaseHealthCheck):
    """Health-Check for externe API-Abhängigkeiten."""

    def __init__(
        self,
        name: str,
        url: str,
        expected_status: int = 200,
        headers: Optional[Dict[str, str]] = None,
        **kwargs: Any,
    ) -> None:
        """Initializes API Health Check.

        Args:
            name: Name of the Checks
            url: API-URL for Health-Check
            expected_status: Erwarteter HTTP-Status
            headers: HTTP-Headers for Request
            **kwargs: Zusätzliche Parameter für BaseHealthCheck
        """
        super().__init__(name, **kwargs)
        self.url = url
        self.expected_status = expected_status
        self.headers = headers or {}

    async def check(self) -> HealthCheckResult:
        """Prüft API-Verfügbarkeit."""
        try:
            import httpx

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self.url, headers=self.headers, timeout=self.timeout_seconds
                )

                if response.status_code == self.expected_status:
                    return HealthCheckResult(
                        name=self.name,
                        status=HealthStatus.HEALTHY,
                        message=f"API verfügbar (Status: {response.status_code})",
                        details={
                            "url": self.url,
                            "status_code": response.status_code,
                            "response_time_ms": response.elapsed.total_seconds() * 1000,
                        },
                    )
                return HealthCheckResult(
                    name=self.name,
                    status=HealthStatus.DEGRADED,
                    message=f"API unerwarteter Status: {response.status_code}",
                    details={
                        "url": self.url,
                        "status_code": response.status_code,
                        "expected_status": self.expected_status,
                    },
                )

        except Exception as e:
            return HealthCheckResult(
                name=self.name,
                status=HealthStatus.UNHEALTHY,
                message=f"API nicht erreichbar: {e!s}",
                error=str(e),
            )


class MemoryHealthCheck(BaseHealthCheck):
    """Health-Check for Speicherverbrauch."""

    def __init__(
        self,
        name: str = "memory",
        warning_threshold: float = 0.8,
        critical_threshold: float = 0.95,
        **kwargs: Any,
    ) -> None:
        """Initializes Memory Health Check.

        Args:
            name: Name of the Checks
            warning_threshold: Warnschwelle (0.0-1.0)
            critical_threshold: Kritische Schwelle (0.0-1.0)
            **kwargs: Tosätzliche parameters for BaseHealthCheck
        """
        super().__init__(name, **kwargs)
        self.warning_threshold = warning_threshold
        self.critical_threshold = critical_threshold

    async def check(self) -> HealthCheckResult:
        """Checks Speicherverbrauch."""
        try:
            import psutil

            memory = psutil.virtual_memory()
            usage_percent = memory.percent / 100.0

            if usage_percent >= self.critical_threshold:
                status = HealthStatus.UNHEALTHY
                message = f"Kritischer Speicherverbrauch: {usage_percent:.1%}"
            elif usage_percent >= self.warning_threshold:
                status = HealthStatus.DEGRADED
                message = f"Hoher Speicherverbrauch: {usage_percent:.1%}"
            else:
                status = HealthStatus.HEALTHY
                message = f"Speicherverbrauch normal: {usage_percent:.1%}"

            return HealthCheckResult(
                name=self.name,
                status=status,
                message=message,
                details={
                    "usage_percent": usage_percent,
                    "total_mb": memory.total // (1024 * 1024),
                    "available_mb": memory.available // (1024 * 1024),
                    "used_mb": memory.used // (1024 * 1024),
                    "warning_threshold": self.warning_threshold,
                    "critical_threshold": self.critical_threshold,
                },
            )

        except ImportError:
            return HealthCheckResult(
                name=self.name,
                status=HealthStatus.UNKNOWN,
                message="psutil not available for Speicher-monitoring",
            )
        except Exception as e:
            return HealthCheckResult(
                name=self.name,
                status=HealthStatus.UNHEALTHY,
                message=f"Speicher-Check failed: {e!s}",
                error=str(e),
            )


@dataclass
class HealthCheckSummary:
    """Tosammenfassung allr Health-Checks.

    Attributes:
        overall_status: Gesamtstatus of the Systems
        total_checks: Atzahl throughgeführter Checks
        healthy_count: Atzahl gesatthe Komponenten
        degraded_count: Atzahl ageschränkter Komponenten
        unhealthy_count: Atzahl ungesatthe Komponenten
        unknown_count: Atzahl unbekatnter status
        checks: lis allr Check-resultse
        timestamp: Zeitpunkt the Tosammenfassung
        duration_ms: Gesamtdauer allr Checks
    """

    overall_status: HealthStatus
    total_checks: int
    healthy_count: int
    degraded_count: int
    unhealthy_count: int
    unknown_count: int
    checks: List[HealthCheckResult]
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    duration_ms: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        """Konvertiert Summary to dictionary.

        Returns:
            dictionary-Repräsentation the Summary
        """
        return {
            "overall_status": self.overall_status.value,
            "total_checks": self.total_checks,
            "healthy_count": self.healthy_count,
            "degraded_count": self.degraded_count,
            "unhealthy_count": self.unhealthy_count,
            "unknown_count": self.unknown_count,
            "timestamp": self.timestamp.isoformat(),
            "duration_ms": self.duration_ms,
            "checks": [check.to_dict() for check in self.checks],
        }


class HealthCheckManager:
    """Manager for Health-Check-Orchestrierung.

    Koordiniert mehrere Health-Checks, berechnet Gesamtstatus
    and bietet monitoring-Integration for Enterprise-Deployments.
    """

    def __init__(self) -> None:
        """Initializes Health Check Manager."""
        self.checks: List[BaseHealthCheck] = []
        self.last_summary: Optional[HealthCheckSummary] = None

    def register_check(self, check: BaseHealthCheck) -> None:
        """Regisers Health-Check.

        Args:
            check: Health-Check-instatce
        """
        self.checks.append(check)
        _logger.info(
            f"Health-Check registers: {check.name}",
            check_name=check.name,
            critical=check.critical,
            timeout=check.timeout_seconds,
            tags=check.tags,
        )

    def register_checks(self, checks: List[BaseHealthCheck]) -> None:
        """Regisers mehrere Health-Checks.

        Args:
            checks: lis from Health-Check-instatceen
        """
        for check in checks:
            self.register_check(check)

    async def run_all_checks(self) -> HealthCheckSummary:
        """Executes all registersen Health-Checks out.

        Returns:
            Tosammenfassung allr Check-resultse
        """
        start_time = time.time()

        _logger.info(
            f"Starting Health-Checks for {len(self.checks)} Komponenten",
            total_checks=len(self.checks),
        )

        # Führe all Checks paralll out
        tasks = [check.run_check() for check in self.checks]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Veraronte resultse
        check_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                # Erstelle error-Result for Exception
                check_results.append(
                    HealthCheckResult(
                        name=self.checks[i].name,
                        status=HealthStatus.UNHEALTHY,
                        message=f"Health-Check Exception: {result!s}",
                        error=str(result),
                    )
                )
            else:
                check_results.append(result)

        # Berechne Statisiken
        status_counts = {
            HealthStatus.HEALTHY: 0,
            HealthStatus.DEGRADED: 0,
            HealthStatus.UNHEALTHY: 0,
            HealthStatus.UNKNOWN: 0,
        }

        for result in check_results:
            status_counts[result.status] += 1

        # Bestimme Gesamtstatus
        overall_status = self._calculate_overall_status(check_results)

        # Erstelle Summary
        duration_ms = (time.time() - start_time) * 1000
        summary = HealthCheckSummary(
            overall_status=overall_status,
            total_checks=len(check_results),
            healthy_count=status_counts[HealthStatus.HEALTHY],
            degraded_count=status_counts[HealthStatus.DEGRADED],
            unhealthy_count=status_counts[HealthStatus.UNHEALTHY],
            unknown_count=status_counts[HealthStatus.UNKNOWN],
            checks=check_results,
            duration_ms=duration_ms,
        )

        self.last_summary = summary

        _logger.info(
            f"Health-Checks abclosed: {overall_status.value}",
            overall_status=overall_status.value,
            total_checks=summary.total_checks,
            healthy=summary.healthy_count,
            degraded=summary.degraded_count,
            unhealthy=summary.unhealthy_count,
            unknown=summary.unknown_count,
            duration_ms=duration_ms,
        )

        return summary

    def _calculate_overall_status(self, results: List[HealthCheckResult]) -> HealthStatus:
        """Berechnet Gesamtstatus basierend on azelnen Check-resultsen.

        Args:
            results: lis allr Check-resultse

        Returns:
            Gesamtstatus of the Systems
        """
        # Prüfe kritische Checks
        critical_checks = [result for result, check in zip(results, self.checks) if check.critical]

        # If kritische Checks unhealthy are, is Gesamtstatus unhealthy
        if any(result.status == HealthStatus.UNHEALTHY for result in critical_checks):
            return HealthStatus.UNHEALTHY

        # If irgenda Check unhealthy is, is Gesamtstatus degraded
        if any(result.status == HealthStatus.UNHEALTHY for result in results):
            return HealthStatus.DEGRADED

        # If irgenda Check degraded is, is Gesamtstatus degraded
        if any(result.status == HealthStatus.DEGRADED for result in results):
            return HealthStatus.DEGRADED

        # If all Checks healthy are, is Gesamtstatus healthy
        if all(result.status == HealthStatus.HEALTHY for result in results):
            return HealthStatus.HEALTHY

        # Fallback for unbekatnte status
        return HealthStatus.UNKNOWN

    def get_last_summary(self) -> Optional[HealthCheckSummary]:
        """Gibt letzte Health-Check-Summary torück.

        Returns:
            Letzte Summary or None
        """
        return self.last_summary


# Globaler Health Check Manager
_health_manager: Optional[HealthCheckManager] = None


def get_health_manager() -> HealthCheckManager:
    """Gibt globalen Health Check Manager torück.

    Returns:
        Health Check Manager instatce
    """
    global _health_manager

    if _health_manager is None:
        _health_manager = HealthCheckManager()

    return _health_manager


__all__ = [
    "APIHealthCheck",
    "BaseHealthCheck",
    "DatabaseHealthCheck",
    "HealthCheckManager",
    "HealthCheckResult",
    "HealthCheckSummary",
    "HealthStatus",
    "MemoryHealthCheck",
    "get_health_manager",
]
