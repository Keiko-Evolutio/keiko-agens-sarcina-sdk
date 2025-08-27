# 🐍 Setup Python Environment Action

Eine wiederverwendbare GitHub Action für standardisiertes Python-Setup mit Dependency-Management und Caching.

## 🎯 Features

- **Flexible Python-Versionen**: Unterstützt alle Python-Versionen
- **Intelligentes Caching**: Automatisches pip-Caching für schnellere Builds
- **Dependency-Management**: Automatische Installation von Projekt- und Dev-Dependencies
- **Editable Installation**: Unterstützt editable und normale Installation
- **Umfassende Validierung**: Verifiziert Installation und Import-Fähigkeit
- **Flexible Konfiguration**: Viele Optionen für verschiedene Use Cases

## 📋 Inputs

| Input | Beschreibung | Required | Default |
|-------|-------------|----------|---------|
| `python-version` | Python-Version | ❌ | '3.11' |
| `cache-dependency-path` | Pfad zu Dependency-Dateien | ❌ | 'pyproject.toml' |
| `install-dependencies` | Projekt-Dependencies installieren | ❌ | 'true' |
| `install-dev-dependencies` | Dev-Dependencies installieren | ❌ | 'true' |
| `install-test-dependencies` | Test-Dependencies installieren | ❌ | 'false' |
| `extra-dependencies` | Zusätzliche Dependencies | ❌ | '' |
| `working-directory` | Arbeitsverzeichnis | ❌ | '.' |
| `pip-cache-enabled` | Pip-Caching aktivieren | ❌ | 'true' |
| `upgrade-pip` | Pip upgraden | ❌ | 'true' |
| `install-editable` | Editable Installation | ❌ | 'true' |

## 📤 Outputs

| Output | Beschreibung |
|--------|-------------|
| `python-version` | Installierte Python-Version |
| `cache-hit` | Ob Cache getroffen wurde |
| `pip-version` | Installierte pip-Version |
| `dependencies-installed` | Ob Dependencies erfolgreich installiert wurden |

## 🚀 Usage

### Basis-Setup

```yaml
- name: 🐍 Setup Python Environment
  uses: ./.github/actions/setup-python-env
  with:
    python-version: '3.11'
```

### Erweiterte Konfiguration

```yaml
- name: 🐍 Setup Python Environment
  uses: ./.github/actions/setup-python-env
  with:
    python-version: '3.11'
    install-dev-dependencies: 'true'
    install-test-dependencies: 'true'
    extra-dependencies: 'mypy bandit safety'
    working-directory: 'backend'
```

### Nur Python ohne Dependencies

```yaml
- name: 🐍 Setup Python Only
  uses: ./.github/actions/setup-python-env
  with:
    python-version: '3.9'
    install-dependencies: 'false'
    pip-cache-enabled: 'false'
```

### Matrix-Build

```yaml
strategy:
  matrix:
    python-version: ['3.9', '3.10', '3.11', '3.12']

steps:
- name: 🐍 Setup Python ${{ matrix.python-version }}
  uses: ./.github/actions/setup-python-env
  with:
    python-version: ${{ matrix.python-version }}
    install-dev-dependencies: 'true'
```

## 🔧 Dependency-Extras

Die Action unterstützt automatische Installation von Extras:

```yaml
# Nur Dev-Dependencies
install-dev-dependencies: 'true'
install-test-dependencies: 'false'
# Installiert: pip install -e ".[dev]"

# Dev + Test Dependencies
install-dev-dependencies: 'true'
install-test-dependencies: 'true'
# Installiert: pip install -e ".[dev,test]"

# Nur Test-Dependencies
install-dev-dependencies: 'false'
install-test-dependencies: 'true'
# Installiert: pip install -e ".[test]"
```

## 📊 Caching

Die Action nutzt automatisches pip-Caching basierend auf:
- `pyproject.toml` (Standard)
- Benutzerdefinierte `cache-dependency-path`
- Python-Version
- OS-Version

Cache-Verhalten:
```yaml
# Cache aktiviert (Standard)
pip-cache-enabled: 'true'
cache-dependency-path: 'pyproject.toml'

# Cache deaktiviert
pip-cache-enabled: 'false'

# Custom Cache-Pfad
cache-dependency-path: 'requirements.txt'
```

## 🧪 Validierung

Die Action führt automatische Validierung durch:

1. **Python-Installation**: Verifiziert Python-Version
2. **Pip-Installation**: Prüft pip-Version
3. **Dependency-Installation**: Validiert erfolgreiche Installation
4. **Import-Test**: Testet Import der installierten Pakete
5. **Environment-Check**: Zeigt Python-Pfade und installierte Pakete

## 🔍 Debugging

Für Debugging-Zwecke:

```yaml
- name: 🐍 Setup Python (Debug)
  uses: ./.github/actions/setup-python-env
  with:
    python-version: '3.11'
  env:
    RUNNER_DEBUG: 1  # Aktiviert Debug-Modus
```

Debug-Output enthält:
- Installierte Pakete (`pip list`)
- Python-Pfade
- Arbeitsverzeichnis
- Python-Executable-Pfad
- Import-Tests

## 🚨 Error Handling

Die Action behandelt häufige Fehler:

- **Import-Fehler**: Warnt bei fehlgeschlagenen Imports
- **Dependency-Konflikte**: Zeigt pip-Konflikte an
- **Cache-Probleme**: Fallback bei Cache-Fehlern
- **Version-Inkompatibilität**: Warnt bei Versions-Problemen

## 📈 Performance

Typische Ausführungszeiten:
- **Mit Cache-Hit**: 30-60 Sekunden
- **Ohne Cache**: 2-5 Minuten
- **Erste Installation**: 3-8 Minuten

Optimierungen:
- Pip-Caching reduziert Installationszeit um 70%+
- Parallele Dependency-Resolution
- Optimierte Cache-Keys

## 🔄 Integration

Verwendung in verschiedenen Workflows:

### CI/CD Pipeline
```yaml
- uses: ./.github/actions/setup-python-env
  with:
    install-dev-dependencies: 'true'
    install-test-dependencies: 'true'
```

### Security Scanning
```yaml
- uses: ./.github/actions/setup-python-env
  with:
    extra-dependencies: 'bandit safety pip-audit'
```

### Documentation Build
```yaml
- uses: ./.github/actions/setup-python-env
  with:
    extra-dependencies: 'mkdocs mkdocs-material'
```

### Release Build
```yaml
- uses: ./.github/actions/setup-python-env
  with:
    install-dev-dependencies: 'false'
    extra-dependencies: 'build twine'
```

## 🤝 Contributing

1. Teste Änderungen mit verschiedenen Python-Versionen
2. Validiere Cache-Verhalten
3. Prüfe Dependency-Installation
4. Dokumentiere neue Features
5. Erstelle Tests für Edge Cases
