"""
KEI Agent Caching Module

Dieses Modul stellt verschiedene Caching-Implementierungen für das KEI Agent SDK bereit.
"""

from __future__ import annotations

# Cache Framework
from .cache_framework import CacheBackend, CacheConfig, CacheFramework

# Cache Manager
from .cache_manager import CacheManager, CacheStrategy

# Specific Cache Implementations
from .memory_cache import MemoryCache
from .multi_level_cache import MultiLevelCache
from .persistent_cache import PersistentCache
from .redis_cache import RedisCache

# Specialized Caches
from .specialized_caches import (
    CapabilityCache,
    ConfigurationCache,
    DiscoveryCache,
    MetricsCache,
)

__all__ = [
    # Framework
    "CacheFramework",
    "CacheBackend",
    "CacheConfig",
    # Manager
    "CacheManager",
    "CacheStrategy",
    # Implementations
    "MemoryCache",
    "PersistentCache",
    "RedisCache",
    "MultiLevelCache",
    # Specialized
    "CapabilityCache",
    "DiscoveryCache",
    "ConfigurationCache",
    "MetricsCache",
]
