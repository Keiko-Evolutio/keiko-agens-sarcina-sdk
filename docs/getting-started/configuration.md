# Konfiguration

Client-Setup und Konfigurationsoptionen für das KEI-Agent SDK.

## 🔧 Basis-Konfiguration

```python
from kei_agent import AgentClientConfig

config = AgentClientConfig(
    base_url="https://api.kei-framework.com",
    api_token="your-api-token",
    agent_id="my-agent",
    timeout=30,
    max_retries=3
)
```

## 🔌 Protokoll-Konfiguration

```python
from kei_agent import ProtocolConfig

protocol_config = ProtocolConfig(
    rpc_enabled=True,
    stream_enabled=True,
    bus_enabled=True,
    mcp_enabled=True,
    auto_protocol_selection=True
```

## 🛡️ Sicherheit

```python
from kei_agent import SecurityConfig, AuthType

security_config = SecurityConfig(
    auth_type=AuthType.BEARER,
    api_token="your-token",
    rbac_enabled=True,
    audit_enabled=True
)
    token_refresh_enabled=True,
    token_cache_ttl=3600
)

# mTLS Authentifizierung
mtls_config = SecurityConfig(
    auth_type=AuthType.MTLS,
    mtls_cert_path="/path/to/client.crt",
    mtls_key_path="/path/to/client.key",
    mtls_ca_path="/path/to/ca.crt"
)
```

#### Security Features

```python
# Enterprise Security (using environment variables)
import os
enterprise_security = SecurityConfig(
    auth_type=AuthType.BEARER,
    api_token=os.getenv("KEI_API_TOKEN"),  # Never hardcode tokens!
    rbac_enabled=True,        # Role-Based Access Control
    audit_enabled=True,       # Audit-Logging
    token_refresh_enabled=True,  # Automatische Token-Erneuerung
    token_cache_ttl=1800     # 30 Minuten Cache
)
```

## 🌍 Umgebungs-spezifische Konfiguration

### Development

```python
from kei_agent import UnifiedKeiAgentClient, AgentClientConfig, ProtocolConfig

# Development-Konfiguration (using environment variables)
import os
dev_config = AgentClientConfig(
    base_url=os.getenv("KEI_API_URL", "http://localhost:8000"),
    api_token=os.getenv("KEI_API_TOKEN"),  # Set via environment variable
    agent_id=os.getenv("KEI_AGENT_ID", "dev-agent"),
    timeout=10,
    max_retries=1
)

dev_protocols = ProtocolConfig(
    rpc_enabled=True,
    stream_enabled=False,  # Vereinfacht für Development
    bus_enabled=False,
    mcp_enabled=True,
    auto_protocol_selection=False
)
```

### Staging

```python
# Staging-Konfiguration
staging_config = AgentClientConfig(
    base_url="https://staging-api.kei-framework.com",
    api_token="staging-token",
    agent_id="staging-agent",
    timeout=20,
    max_retries=2
)

staging_protocols = ProtocolConfig(
    rpc_enabled=True,
    stream_enabled=True,
    bus_enabled=True,
    mcp_enabled=True,
    auto_protocol_selection=True,
    protocol_fallback_enabled=False  # Explizite Fehler in Staging
)
```

### Production

```python
# Production-Konfiguration
prod_config = AgentClientConfig(
    base_url="https://api.kei-framework.com",
    api_token="prod-token",
    agent_id="prod-agent-001",
    timeout=30,
    max_retries=5,
    retry_delay=2.0
)

prod_protocols = ProtocolConfig(
    rpc_enabled=True,
    stream_enabled=True,
    bus_enabled=True,
    mcp_enabled=True,
    auto_protocol_selection=True,
    protocol_fallback_enabled=True  # Maximale Resilience
)

prod_security = SecurityConfig(
    auth_type=AuthType.OIDC,
    oidc_issuer="https://auth.company.com",
    oidc_client_id="prod-client",
    oidc_client_secret="prod-secret",
    rbac_enabled=True,
    audit_enabled=True,
    token_refresh_enabled=True
)
```

## 📁 Konfiguration aus Dateien

### YAML-Konfiguration

```yaml
# config.yaml
agent:
  base_url: "https://api.kei-framework.com"
  api_token: "${KEI_API_TOKEN}"
  agent_id: "yaml-configured-agent"
  timeout: 30
  max_retries: 3

protocols:
  rpc_enabled: true
  stream_enabled: true
  bus_enabled: true
  mcp_enabled: true
  auto_protocol_selection: true
  protocol_fallback_enabled: true

security:
  auth_type: "bearer"
  rbac_enabled: true
  audit_enabled: true
```

```python
import yaml
import os
from kei_agent import AgentClientConfig, ProtocolConfig, SecurityConfig, AuthType

def load_config_from_yaml(file_path: str):
    """Lädt Konfiguration aus YAML-Datei."""
    with open(file_path, 'r') as f:
        config_data = yaml.safe_load(f)

    # Umgebungsvariablen ersetzen
    api_token = os.getenv('KEI_API_TOKEN', config_data['agent']['api_token'])

    agent_config = AgentClientConfig(
        base_url=config_data['agent']['base_url'],
        api_token=api_token,
        agent_id=config_data['agent']['agent_id'],
        timeout=config_data['agent']['timeout'],
        max_retries=config_data['agent']['max_retries']
    )

    protocol_config = ProtocolConfig(**config_data['protocols'])

    security_config = SecurityConfig(
        auth_type=AuthType(config_data['security']['auth_type']),
        api_token=api_token,
        rbac_enabled=config_data['security']['rbac_enabled'],
        audit_enabled=config_data['security']['audit_enabled']
    )

    return agent_config, protocol_config, security_config

# Verwendung
agent_config, protocol_config, security_config = load_config_from_yaml('config.yaml')
```

### JSON-Konfiguration

```json
{
  "agent": {
    "base_url": "https://api.kei-framework.com",
    "api_token": "${KEI_API_TOKEN}",
    "agent_id": "json-configured-agent",
    "timeout": 30,
    "max_retries": 3
  },
  "protocols": {
    "rpc_enabled": true,
    "stream_enabled": true,
    "bus_enabled": true,
    "mcp_enabled": true,
    "auto_protocol_selection": true,
    "protocol_fallback_enabled": true
  },
  "security": {
    "auth_type": "bearer",
    "rbac_enabled": true,
    "audit_enabled": true
  }
}
```

## 🔐 Umgebungsvariablen

### Standard-Umgebungsvariablen

```bash
# Basis-Konfiguration
export KEI_API_URL="https://api.kei-framework.com"
export KEI_API_TOKEN="your-api-token"
export KEI_AGENT_ID="env-configured-agent"

# Erweiterte Konfiguration
export KEI_TIMEOUT="30"
export KEI_MAX_RETRIES="3"
export KEI_RETRY_DELAY="1.0"

# Protokoll-Konfiguration
export KEI_RPC_ENABLED="true"
export KEI_STREAM_ENABLED="true"
export KEI_BUS_ENABLED="true"
export KEI_MCP_ENABLED="true"

# Security
export KEI_AUTH_TYPE="bearer"
export KEI_RBAC_ENABLED="true"
export KEI_AUDIT_ENABLED="true"
```

### Konfiguration aus Umgebungsvariablen

```python
import os
from kei_agent import AgentClientConfig, ProtocolConfig, SecurityConfig, AuthType

def config_from_env():
    """Erstellt Konfiguration aus Umgebungsvariablen."""
    agent_config = AgentClientConfig(
        base_url=os.getenv('KEI_API_URL', 'https://api.kei-framework.com'),
        api_token=os.getenv('KEI_API_TOKEN'),
        agent_id=os.getenv('KEI_AGENT_ID', 'default-agent'),
        timeout=float(os.getenv('KEI_TIMEOUT', '30')),
        max_retries=int(os.getenv('KEI_MAX_RETRIES', '3')),
        retry_delay=float(os.getenv('KEI_RETRY_DELAY', '1.0'))
    )

    protocol_config = ProtocolConfig(
        rpc_enabled=os.getenv('KEI_RPC_ENABLED', 'true').lower() == 'true',
        stream_enabled=os.getenv('KEI_STREAM_ENABLED', 'true').lower() == 'true',
        bus_enabled=os.getenv('KEI_BUS_ENABLED', 'true').lower() == 'true',
        mcp_enabled=os.getenv('KEI_MCP_ENABLED', 'true').lower() == 'true'
    )

    security_config = SecurityConfig(
        auth_type=AuthType(os.getenv('KEI_AUTH_TYPE', 'bearer')),
        api_token=os.getenv('KEI_API_TOKEN'),
        rbac_enabled=os.getenv('KEI_RBAC_ENABLED', 'true').lower() == 'true',
        audit_enabled=os.getenv('KEI_AUDIT_ENABLED', 'true').lower() == 'true'
    )

    return agent_config, protocol_config, security_config

# Verwendung
agent_config, protocol_config, security_config = config_from_env()
```

## 🔧 Erweiterte Konfiguration

### Custom Configuration Factory

```python
from typing import Optional
from kei_agent import UnifiedKeiAgentClient, AgentClientConfig, ProtocolConfig, SecurityConfig

class KEIAgentConfigFactory:
    """Factory für KEI-Agent-Konfigurationen."""

    @staticmethod
    def create_development_client() -> UnifiedKeiAgentClient:
        """Erstellt Development-Client."""
        config = AgentClientConfig(
            base_url="http://localhost:8000",
            api_token="dev-token",
            agent_id="dev-agent",
            timeout=10
        )
        return UnifiedKeiAgentClient(config=config)

    @staticmethod
    def create_production_client(
        api_token: str,
        agent_id: str,
        base_url: Optional[str] = None
    ) -> UnifiedKeiAgentClient:
        """Erstellt Production-Client."""
        agent_config = AgentClientConfig(
            base_url=base_url or "https://api.kei-framework.com",
            api_token=api_token,
            agent_id=agent_id,
            timeout=30,
            max_retries=5
        )

        protocol_config = ProtocolConfig(
            auto_protocol_selection=True,
            protocol_fallback_enabled=True
        )

        security_config = SecurityConfig(
            auth_type=AuthType.BEARER,
            api_token=api_token,
            rbac_enabled=True,
            audit_enabled=True
        )

        return UnifiedKeiAgentClient(
            config=agent_config,
            protocol_config=protocol_config,
            security_config=security_config
        )

# Verwendung
dev_client = KEIAgentConfigFactory.create_development_client()
prod_client = KEIAgentConfigFactory.create_production_client(
    api_token="prod-token",
    agent_id="prod-agent-001"
)
```

## 🚨 Konfiguration validieren

```python
async def validate_configuration():
    """Validiert Client-Konfiguration."""
    try:
        config = AgentClientConfig(
            base_url="https://api.kei-framework.com",
            api_token="test-token",
            agent_id="validation-test"
        )

        async with UnifiedKeiAgentClient(config=config) as client:
            # Basis-Validierung
            info = client.get_client_info()
            print(f"✅ Client konfiguriert: {info['agent_id']}")

            # Protokoll-Validierung
            protocols = client.get_available_protocols()
            print(f"✅ Verfügbare Protokolle: {protocols}")

            # Health Check
            health = await client.health_check()
            print(f"✅ Health Status: {health.get('status', 'unknown')}")

    except Exception as e:
        print(f"❌ Konfigurationsfehler: {e}")

# Ausführen
import asyncio
asyncio.run(validate_configuration())
```

---

**Nächster Schritt:** [Basis-Konzepte →](../user-guide/concepts.md)
