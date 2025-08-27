# 📢 GitHub Actions Notifications

Umfassendes Notification-System für kritische Workflow-Failures im KEI-Agent Python SDK.

## 🎯 Übersicht

Das Notification-System benachrichtigt automatisch über kritische Workflow-Fehler via:
- **Slack** - Strukturierte Nachrichten mit Rich-Formatting
- **Microsoft Teams** - Adaptive Cards mit allen relevanten Details
- **GitHub Issues** - Automatische Issue-Erstellung für Tracking

## 🏗️ Architektur

### Composite Action
- **Location:** `.github/actions/notify-failure/`
- **Wiederverwendbar** für alle Workflows
- **Konfigurierbar** für verschiedene Severity-Level
- **Intelligent** - Event-basierte Filterung

### Integrierte Workflows

| Workflow | Severity | Trigger | Beschreibung |
|----------|----------|---------|-------------|
| `ci.yml` | High/Critical | Push, Schedule | Haupt-CI-Pipeline |
| `security.yml` | Critical | Push, Schedule, PR | Security-Scans |
| `chaos-testing.yml` | High | Schedule, PR | Chaos Engineering |
| `dependency-management.yml` | Medium | Schedule | Dependency-Updates |

## 🔧 Setup

### 1. Slack Webhook konfigurieren

```bash
# 1. Slack App erstellen oder bestehende verwenden
# 2. Incoming Webhooks aktivieren
# 3. Webhook für Channel erstellen
# 4. Secret hinzufügen
gh secret set SLACK_WEBHOOK_URL --body "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"
```

### 2. Microsoft Teams Webhook konfigurieren

```bash
# 1. Teams Channel öffnen
# 2. "..." → "Connectors" → "Incoming Webhook"
# 3. Webhook konfigurieren und URL kopieren
# 4. Secret hinzufügen
gh secret set TEAMS_WEBHOOK_URL --body "https://outlook.office.com/webhook/..."
```

### 3. Secrets validieren

```bash
# Prüfe ob Secrets gesetzt sind
gh secret list

# Teste Webhook (optional)
curl -X POST -H "Content-Type: application/json" \
  -d '{"text": "Test notification from KEI-Agent"}' \
  "$SLACK_WEBHOOK_URL"
```

## 📋 Notification-Konfiguration

### Severity-Level

```yaml
# Kritisch - Immer benachrichtigen + Issue erstellen
severity: "critical"

# Hoch - Conditional benachrichtigen + Issue erstellen  
severity: "high"

# Mittel - Conditional benachrichtigen + Issue erstellen
severity: "medium"

# Niedrig - Conditional benachrichtigen, kein Issue
severity: "low"
```

### Event-basierte Filterung

```yaml
# Benachrichtigungen konfigurieren
notify_on_schedule: "true"   # Geplante Workflows
notify_on_push: "true"       # Push-Events
notify_on_pr: "false"        # Pull Requests
```

### Beispiel-Integration

```yaml
- name: 📢 Notify on failure
  if: failure()
  uses: ./.github/actions/notify-failure
  with:
    workflow_name: ${{ github.workflow }}
    job_name: ${{ github.job }}
    failure_reason: "Detailed failure description"
    severity: "high"
    slack_webhook_url: ${{ secrets.SLACK_WEBHOOK_URL }}
    teams_webhook_url: ${{ secrets.TEAMS_WEBHOOK_URL }}
    notify_on_push: "true"
    notify_on_schedule: "true"
    notify_on_pr: "false"
```

## 🎨 Notification-Formate

### Slack Notification

```json
{
  "attachments": [
    {
      "color": "#FF0000",
      "blocks": [
        {
          "type": "header",
          "text": {
            "type": "plain_text", 
            "text": "🚨 Workflow Failure - CRITICAL Priority"
          }
        },
        {
          "type": "section",
          "fields": [
            {
              "type": "mrkdwn",
              "text": "*Repository:*\nkeiko-dev/kei-agent-py-sdk"
            },
            {
              "type": "mrkdwn", 
              "text": "*Workflow:*\nCI/CD Pipeline"
            },
            {
              "type": "mrkdwn",
              "text": "*Job:*\ncomprehensive-tests"
            },
            {
              "type": "mrkdwn",
              "text": "*Branch:*\nmain"
            }
          ]
        },
        {
          "type": "actions",
          "elements": [
            {
              "type": "button",
              "text": {
                "type": "plain_text",
                "text": "View Workflow Run"
              },
              "url": "https://github.com/repo/actions/runs/123456",
              "style": "danger"
            }
          ]
        }
      ]
    }
  ]
}
```

### Teams Notification

```json
{
  "@type": "MessageCard",
  "@context": "http://schema.org/extensions",
  "themeColor": "#FF0000",
  "summary": "Workflow Failure: CI/CD Pipeline",
  "sections": [
    {
      "activityTitle": "🚨 Workflow Failure - CRITICAL Priority",
      "activitySubtitle": "keiko-dev/kei-agent-py-sdk",
      "facts": [
        {
          "name": "Workflow",
          "value": "CI/CD Pipeline"
        },
        {
          "name": "Job", 
          "value": "comprehensive-tests"
        },
        {
          "name": "Branch",
          "value": "main"
        },
        {
          "name": "Triggered by",
          "value": "push"
        }
      ]
    }
  ],
  "potentialAction": [
    {
      "@type": "OpenUri",
      "name": "View Workflow Run",
      "targets": [
        {
          "os": "default",
          "uri": "https://github.com/repo/actions/runs/123456"
        }
      ]
    }
  ]
}
```

## 🔍 Monitoring & Debugging

### Workflow-Logs prüfen

```bash
# Notification-Step-Logs anzeigen
gh run view <run-id> --log

# Spezifischen Job anzeigen
gh run view <run-id> --job <job-id>
```

### Webhook-Testing

```bash
# Slack Webhook testen
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "text": "Test notification",
    "attachments": [
      {
        "color": "#FF0000",
        "text": "This is a test notification from KEI-Agent"
      }
    ]
  }' \
  "$SLACK_WEBHOOK_URL"

# Teams Webhook testen  
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "@type": "MessageCard",
    "@context": "http://schema.org/extensions",
    "summary": "Test notification",
    "text": "This is a test notification from KEI-Agent"
  }' \
  "$TEAMS_WEBHOOK_URL"
```

### Häufige Probleme

| Problem | Lösung |
|---------|--------|
| Webhook 404 | URL prüfen, Webhook neu erstellen |
| Keine Benachrichtigung | Event-Filter prüfen (`notify_on_*`) |
| Formatting-Fehler | JSON-Syntax validieren |
| Permission-Fehler | GitHub Token Berechtigungen prüfen |

## 📊 Metriken & Analytics

### Notification-Erfolg tracken

```yaml
- name: 📊 Track notification metrics
  if: always()
  run: |
    echo "Notification sent: ${{ steps.notify.outputs.notification_sent }}"
    echo "Issue created: ${{ steps.notify.outputs.issue_created }}"
    echo "Issue number: ${{ steps.notify.outputs.issue_number }}"
```

### Dashboard-Integration

Die Notifications können in externe Monitoring-Dashboards integriert werden:
- **Grafana** - Webhook-basierte Alerts
- **DataDog** - Custom Events
- **PagerDuty** - Incident-Management

## 🔒 Security

### Best Practices

1. **Webhook URLs als Secrets** speichern
2. **Minimale Token-Berechtigungen** verwenden
3. **Keine sensiblen Daten** in Nachrichten
4. **Webhook-URLs regelmäßig rotieren**
5. **Access-Logs überwachen**

### Secret-Management

```bash
# Secrets rotieren
gh secret set SLACK_WEBHOOK_URL --body "new-webhook-url"
gh secret set TEAMS_WEBHOOK_URL --body "new-webhook-url"

# Secrets auflisten (ohne Werte)
gh secret list

# Secret löschen
gh secret delete OLD_WEBHOOK_URL
```

## 🚀 Erweiterte Features

### Custom Notification-Handler

```yaml
# Eigene Notification-Logik
- name: 📢 Custom notification
  if: failure()
  run: |
    # Custom notification script
    python scripts/custom_notify.py \
      --workflow "${{ github.workflow }}" \
      --job "${{ github.job }}" \
      --severity "high"
```

### Conditional Notifications

```yaml
# Nur bei main-Branch benachrichtigen
- name: 📢 Notify on main failure
  if: failure() && github.ref == 'refs/heads/main'
  uses: ./.github/actions/notify-failure
  with:
    severity: "critical"
    notify_on_push: "true"

# Nur bei bestimmten Dateien
- name: 📢 Notify on core changes
  if: failure() && contains(github.event.head_commit.modified, 'kei_agent/core/')
  uses: ./.github/actions/notify-failure
  with:
    severity: "high"
```

## 📝 Changelog

### v1.0.0 (2025-08-27)
- Initial implementation
- Slack und Teams Support
- GitHub Issue Integration
- Severity-basierte Filterung
- Event-basierte Conditional Notifications
- Integration in kritische Workflows
