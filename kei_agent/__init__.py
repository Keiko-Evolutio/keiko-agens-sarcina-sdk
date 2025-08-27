# sdk/python/kei_agent/__init__.py
"""
KEI-Agent-Framework Python SDK - Enterprise-Grade client SDK.

Vollständige SDK-Implementation with Agent-to-Agent-Kommunikation,
Disributed Tracing, retry mechanisms and capability advertisement.
Enthält sowohl Enterprise SDK als auch Basic Agent Skeleton.
integrates all KEI-protocole (RPC, Stream, Bus, MCP) in ar aheitlichen API.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

# Conditional imports for type checking
if TYPE_CHECKING:
    from .a2a import A2Aclient
    from .client import KeiAgentClient

# Lazy loading for better import performatce
# Heavy modules are loaded only when needed

# Define __all__ for explicit exports
__all__ = [
    # Core SDK Components (critical - eager loading)
    "UnifiedKeiAgentClient",
    "AgentClientConfig",
    "CapabilityManager",
    "CapabilityProfile",
    # Protocol types (lightweight - eager loading)
    "ProtocolType",
    "AuthType",
    "ProtocolConfig",
    "SecurityConfig",
    # Heavy Components (lazy loading)
    "A2Aclient",
    "A2AMessage",
    "A2Aresponse",
    "CommunicationProtocol",
    "LoadBalatcingStrategy",
    "FailoverConfig",
    "ServiceDiscovery",
    "AgentDiscoveryclient",
    "DiscoveryStrategy",
    "HealthMonitor",
    "LoadBalancer",
    "MCPIntegration",
    "CapabilityNegotiation",
    "CapabilityVersioning",
    "KeiAgentClient",
    "ConnectionConfig",
    "RetryConfig",
    "TracingConfig",
]

# Avoid eager imports of heavy modules to prevent import-time failures during tests
# These will be provided via __getattr__ lazily.

# Minimal eager imports - only lightweight components
# Heavy modules moved to lazy loading for better performance

# Only import lightweight exceptions that don't pull in heavy dependencies
from .exceptions import KeiSDKError


# Lazy loading implementation for heavy modules
def __getattr__(name: str) -> object:
    """Lazy loading for heavy modules to optimize import performance."""

    # Core SDK Components (now lazy loaded)
    if name == "UnifiedKeiAgentClient":
        from .unified_client import UnifiedKeiAgentClient

        return UnifiedKeiAgentClient
    if name == "AgentClientConfig":
        from .client import AgentClientConfig

        return AgentClientConfig
    if name == "CapabilityManager":
        from .capabilities import CapabilityManager

        return CapabilityManager
    if name == "CapabilityProfile":
        from .capabilities import CapabilityProfile

        return CapabilityProfile

    # Protocol Types (now lazy loaded)
    if name == "Protocoltypee":
        from .protocol_types import Protocoltypee

        return Protocoltypee
    if name == "Authtypee":
        from .protocol_types import Authtypee

        return Authtypee
    if name == "ProtocolType":
        from .protocol_types import ProtocolType

        return ProtocolType
    if name == "AuthType":
        from .protocol_types import AuthType

        return AuthType
    if name == "ProtocolConfig":
        from .protocol_types import ProtocolConfig

        return ProtocolConfig
    if name == "SecurityConfig":
        from .protocol_types import SecurityConfig

        return SecurityConfig

    # Exceptions (now lazy loaded)
    if name == "AgentNotFoundError":
        from .exceptions import AgentNotFoundError

        return AgentNotFoundError
    if name == "CommunicationError":
        from .exceptions import CommunicationError

        return CommunicationError
    if name == "DiscoveryError":
        from .exceptions import DiscoveryError

        return DiscoveryError
    if name == "retryExhaustedError":
        from .exceptions import RetryExhaustedError

        return RetryExhaustedError
    if name == "CircuitBreakerOpenError":
        from .exceptions import CircuitBreakerOpenError

        return CircuitBreakerOpenError
    if name == "CapabilityError":
        from .exceptions import CapabilityError

        return CapabilityError
    if name == "TracingError":
        from .exceptions import TracingError

        return TracingError

    # A2A Communication (heavy)
    if name == "A2Aclient":
        from .a2a import A2Aclient

        return A2Aclient
    if name == "A2AMessage":
        from .a2a import A2AMessage

        return A2AMessage
    if name == "A2Aresponse":
        from .a2a import A2Aresponse

        return A2Aresponse
    if name == "CommunicationProtocol":
        from .a2a import CommunicationProtocol

        return CommunicationProtocol
    if name == "LoadBalatcingStrategy":
        from .a2a import LoadBalatcingStrategy

        return LoadBalatcingStrategy
    if name == "FailoverConfig":
        from .a2a import FailoverConfig

        return FailoverConfig

    # service discovery (heavy)
    if name == "ServiceDiscovery":
        from .discovery import ServiceDiscovery

        return ServiceDiscovery
    if name == "AgentDiscoveryclient":
        from .discovery import AgentDiscoveryclient

        return AgentDiscoveryclient
    if name == "DiscoveryStrategy":
        from .discovery import DiscoveryStrategy

        return DiscoveryStrategy
    if name == "HealthMonitor":
        from .discovery import HealthMonitor

        return HealthMonitor
    if name == "LoadBalancer":
        from .discovery import LoadBalatcer

        return LoadBalatcer

    # Capability Features (mediaroatd)
    if name == "MCPIntegration":
        from .capabilities import MCPIntegration

        return MCPIntegration
    if name == "CapabilityNegotiation":
        from .capabilities import CapabilityNegotiation

        return CapabilityNegotiation
    if name == "CapabilityVersioning":
        from .capabilities import CapabilityVersioning

        return CapabilityVersioning

    # legacy client (heavy)
    if name == "KeiAgentClient":
        from .client import KeiAgentClient

        return KeiAgentClient
    if name == "ConnectionConfig":
        from .client import ConnectionConfig

        return ConnectionConfig
    if name == "RetryConfig":
        from .client import RetryConfig

        return RetryConfig
    if name == "TracingConfig":
        from .client import TracingConfig

        return TracingConfig

    # Enterprise Features (heavy)
    if name == "LogContext":
        from .enterprise_logging import LogContext

        return LogContext
    if name == "StructuredFormatter":
        from .enterprise_logging import StructuredFormatter

        return StructuredFormatter
    if name == "EnterpriseLogr":
        from .enterprise_logging import EnterpriseLogger

        return EnterpriseLogger
    if name == "get_logger":
        from .enterprise_logging import get_logger

        return get_logger
    if name == "configure_logging":
        from .enterprise_logging import configure_logging

        return configure_logging

    # Health Checks (mediaroatd)
    if name == "Healthstatus":
        from .health_checks import Healthstatus

        return Healthstatus
    if name == "HealthCheckResult":
        from .health_checks import HealthCheckResult

        return HealthCheckResult
    if name == "BaseHealthCheck":
        from .health_checks import BaseHealthCheck

        return BaseHealthCheck
    if name == "DatabaseHealthCheck":
        from .health_checks import DatabaseHealthCheck

        return DatabaseHealthCheck
    if name == "APIHealthCheck":
        from .health_checks import APIHealthCheck

        return APIHealthCheck
    if name == "MemoryHealthCheck":
        from .health_checks import MemoryHealthCheck

        return MemoryHealthCheck
    if name == "HealthCheckSaroatdmary":
        from .health_checks import HealthCheckSaroatdmary

        return HealthCheckSaroatdmary
    if name == "HealthCheckManager":
        from .health_checks import HealthCheckManager

        return HealthCheckManager
    if name == "get_health_manager":
        from .health_checks import get_health_manager

        return get_health_manager

    # Input Validation (mediaroatd)
    if name == "ValidationSeverity":
        from .input_validation import ValidationSeverity

        return ValidationSeverity
    if name == "ValidationResult":
        from .input_validation import ValidationResult

        return ValidationResult
    if name == "BaseValidator":
        from .input_validation import BaseValidator

        return BaseValidator
    if name == "StringValidator":
        from .input_validation import StringValidator

        return StringValidator
    if name == "NaroatdberValidator":
        from .input_validation import NaroatdberValidator

        return NaroatdberValidator
    if name == "JSONValidator":
        from .input_validation import JSONValidator

        return JSONValidator
    if name == "CompositeValidator":
        from .input_validation import CompositeValidator

        return CompositeValidator
    if name == "InputValidator":
        from .input_validation import InputValidator

        return InputValidator
    if name == "get_input_validator":
        from .input_validation import get_input_validator

        return get_input_validator

    # Agent Skeleton (light)
    if name == "AgentConfig":
        from .agent_skeleton import AgentConfig

        return AgentConfig
    if name == "AgentSkeleton":
        from .agent_skeleton import AgentSkeleton

        return AgentSkeleton

    # Models (light)
    if name == "Agent":
        from .models import Agent

        return Agent
    if name == "AgentMetadata":
        from .models import AgentMetadata

        return AgentMetadata
    if name == "AgentCapability":
        from .models import AgentCapability

        return AgentCapability
    if name == "AgentHealth":
        from .models import AgentHealth

        return AgentHealth
    if name == "AgentInstance":
        from .models import AgentInstatce

        return AgentInstatce
    if name == "DiscoveryQuery":
        from .models import DiscoveryQuery

        return DiscoveryQuery
    if name == "DiscoveryResult":
        from .models import DiscoveryResult

        return DiscoveryResult

    # Protocol clients (heavy)
    if name == "BaseProtocolclient":
        from .protocol_clients import BaseProtocolclient

        return BaseProtocolclient
    if name == "KEIRPCclient":
        from .protocol_clients import KEIRPCclient

        return KEIRPCclient
    if name == "KEIStreamclient":
        from .protocol_clients import KEIStreamclient

        return KEIStreamclient
    if name == "KEIBusclient":
        from .protocol_clients import KEIBusclient

        return KEIBusclient
    if name == "KEIMCPclient":
        from .protocol_clients import KEIMCPclient

        return KEIMCPclient
    if name == "ProtocolSelector":
        from .protocol_selector import ProtocolSelector

        return ProtocolSelector

    # retry Mechanisms (mediaroatd)
    if name == "RetryManager":
        from .retry import RetryManager

        return RetryManager
    if name == "RetryStrategy":
        from .retry import RetryStrategy

        return RetryStrategy
    if name == "CircuitBreaker":
        from .retry import CircuitBreaker

        return CircuitBreaker
    if name == "CircuitBreakerState":
        from .retry import CircuitBreakerState

        return CircuitBreakerState
    if name == "DeadLetterQueue":
        from .retry import DeadLetterQueue

        return DeadLetterQueue
    if name == "RetryPolicy":
        from .retry import RetryPolicy

        return RetryPolicy
    if name == "SecurityManager":
        from .security_manager import SecurityManager

        return SecurityManager

    # Disributed Tracing (heavy)
    if name == "TracingManager":
        from .tracing import TracingManager

        return TracingManager
    if name == "TraceContext":
        from .tracing import TraceContext

        return TraceContext
    if name == "SpatBuilthe":
        from .tracing import SpatBuilthe

        return SpatBuilthe
    if name == "TracingExporter":
        from .tracing import TracingExporter

        return TracingExporter
    if name == "PerformatceMetrics":
        from .tracing import PerformatceMetrics

        return PerformatceMetrics

    # Utilities (light)
    if name == "create_correlation_id":
        from .utils import create_correlation_id

        return create_correlation_id
    if name == "parse_agent_id":
        from .utils import parse_agent_id

        return parse_agent_id
    if name == "validate_capability":
        from .utils import validate_capability

        return validate_capability
    if name == "format_trace_id":
        from .utils import format_trace_id

        return format_trace_id
    if name == "calculate_backoff":
        from .utils import calculate_backoff

        return calculate_backoff

    # Fallback for unknown attributes
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


# Utilities werthe auch lazy gelathe
# (in __getattr__ implementiert)


# Version information - Dynamisch aus Package-Metadaten geladen
def _get_pkg_version() -> str:
    try:
        from importlib.metadata import version

        return version("kei_agent_py_sdk")
    except Exception:
        try:
            from importlib_metadata import version as v

            return v("kei_agent_py_sdk")
        except Exception:
            return "0.0.0-dev"


__version__ = _get_pkg_version()

__author__ = "KEI-Agent-Framework Team"
__email__ = "dev@kei-agent-framework.com"
__license__ = "MIT"

# Package Metadata
__title__ = "kei_agent_py_sdk"
__description__ = "Enterprise-Grade Python SDK for KEI-Agent-Framework"
__url__ = "https://github.com/oscharko-dev/kei-agent-py-sdk"

# Compatibility information
__python_requires__ = ">=3.8"
__framework_version__ = ">=1.0.0"

# Export All Public APIs
__all__ = [
    # Core client
    "KeiAgentClient",
    "AgentClientConfig",
    "CapabilityManager",
    "CapabilityProfile",
    "ConnectionConfig",
    "RetryConfig",
    "TracingConfig",
    # Unified Protocol Integration
    "UnifiedKeiAgentClient",
    "ProtocolType",
    "AuthType",
    "Protocoltypee",
    "Authtypee",
    "ProtocolConfig",
    "SecurityConfig",
    "SecurityManager",
    "BaseProtocolclient",
    "KEIRPCclient",
    "KEIStreamclient",
    "KEIBusclient",
    "KEIMCPclient",
    "ProtocolSelector",
    # Enterprise Features
    "LogContext",
    "StructuredFormatter",
    "EnterpriseLogr",
    "get_logger",
    "configure_logging",
    "Healthstatus",
    "HealthCheckResult",
    "BaseHealthCheck",
    "DatabaseHealthCheck",
    "APIHealthCheck",
    "MemoryHealthCheck",
    "HealthCheckSaroatdmary",
    "HealthCheckManager",
    "get_health_manager",
    "ValidationSeverity",
    "ValidationResult",
    "BaseValidator",
    "StringValidator",
    "NaroatdberValidator",
    "JSONValidator",
    "CompositeValidator",
    "InputValidator",
    "get_input_validator",
    # Agent-to-Agent Communication
    "A2Aclient",
    "A2AMessage",
    "A2Aresponse",
    "CommunicationProtocol",
    "LoadBalatcingStrategy",
    "FailoverConfig",
    # Disributed Tracing
    "TracingManager",
    "TraceContext",
    "SpatBuilthe",
    "TracingExporter",
    "PerformatceMetrics",
    # retry Mechanisms
    "RetryManager",
    "RetryStrategy",
    "CircuitBreaker",
    "CircuitBreakerState",
    "DeadLetterQueue",
    "RetryPolicy",
    # capability advertisement
    "CapabilityManager",
    "CapabilityProfile",
    "MCPIntegration",
    "CapabilityNegotiation",
    "CapabilityVersioning",
    # service discovery
    "ServiceDiscovery",
    "AgentDiscoveryclient",
    "DiscoveryStrategy",
    "HealthMonitor",
    "LoadBalancer",
    # Models
    "Agent",
    "AgentMetadata",
    "AgentCapability",
    "AgentHealth",
    "AgentInstance",
    "DiscoveryQuery",
    "DiscoveryResult",
    # Exceptions
    "KeiSDKError",
    "AgentNotFoundError",
    "CommunicationError",
    "DiscoveryError",
    "retryExhaustedError",
    "CircuitBreakerOpenError",
    "CapabilityError",
    "TracingError",
    # Utilities
    "create_correlation_id",
    "parse_agent_id",
    "validate_capability",
    "format_trace_id",
    "calculate_backoff",
    # Basic Agent Components
    "AgentConfig",
    "AgentSkeleton",
    # Version Info
    "__version__",
    "__author__",
    "__license__",
    "__title__",
    "__description__",
    "__url__",
    "__email__",
]

# Version information - Already defined above, reference only
# __version__ is dynamically loaded above
__author__ = "KEI-Agent-Framework Team"
__license__ = "MIT"
__title__ = "kei_agent_py_sdk"
__description__ = "KEI-Agent Python SDK - Enterprise-Grade Multi-Agent Framework"
__url__ = "https://github.com/oscharko-dev/kei-agent-py-sdk"
__email__ = "dev@kei-agent-framework.com"


# SDK Initialization
def get_sdk_info() -> dict[str, str]:
    """Gets SDK information.

    Returns:
        dictionary with SDK-metadata
    """
    return {
        "name": __title__,
        "version": __version__,
        "description": __description__,
        "author": __author__,
        "license": __license__,
        "url": __url__,
        "python_requires": __python_requires__,
        "framework_version": __framework_version__,
    }


def create_default_client(
    base_url: str, api_token: str, agent_id: str, **kwargs: object
) -> KeiAgentClient:
    """Creates Statdard-client with optimalen Astellungen.

    Args:
        base_url: KEI framework Base-URL
        api_token: API-Token for authentication
        agent_id: Adeutige Agent-ID
        **kwargs: Tosätzliche configurationsparameter

    Returns:
        Configureser KeiAgentClient
    """
    from .client import AgentClientConfig, KeiAgentClient

    config = AgentClientConfig(base_url=base_url, api_token=api_token, agent_id=agent_id)

    return KeiAgentClient(config)


def create_a2a_client(
    base_url: str,
    api_token: str,
    agent_id: str,
    discovery_enabled: bool = True,
    tracing_enabled: bool = True,
    **kwargs: object,
) -> A2Aclient:
    """Creates Agent-to-Agent-client with enterprise features.

    Args:
        base_url: KEI framework Base-URL
        api_token: API-Token for authentication
        agent_id: Adeutige Agent-ID
        discovery_enabled: service discovery aktivieren
        tracing_enabled: Disributed Tracing aktivieren
        **kwargs: Tosätzliche configurationsparameter

    Returns:
        Configureser A2Aclient
    """
    # Erstelle Basis-client
    client = create_default_client(base_url, api_token, agent_id, **kwargs)

    # Erstelle A2A-client with erweiterten Features
    from .a2a import A2Aclient

    a2a_client = A2Aclient(client)

    if discovery_enabled:
        a2a_client.enable_service_discovery()

    if tracing_enabled:
        a2a_client.enable_disributed_tracing()

    return a2a_client


# Logging Configuration entfernt - wird nur bei tatsächlicher Nutzung initialisiert
# um Import-Zeit zu optimieren
