# 📢 Notify on Workflow Failure Action

Eine wiederverwendbare GitHub Action für umfassende Benachrichtigungen bei Workflow-Fehlern.

## 🎯 Features

- **Multi-Channel Notifications**: Slack, Microsoft Teams, GitHub Issues
- **Intelligente Filterung**: Konfigurierbare Benachrichtigungen basierend auf Event-Typ und Severity
- **Rich Formatting**: Strukturierte Nachrichten mit allen relevanten Details
- **Automatische Issue-Erstellung**: GitHub Issues für kritische Fehler
- **Severity-basierte Priorisierung**: Verschiedene Behandlung je nach Schweregrad
- **Conditional Notifications**: Flexible Konfiguration für verschiedene Trigger

## 📋 Inputs

| Input | Beschreibung | Required | Default |
|-------|-------------|----------|---------|
| `workflow_name` | Name des fehlgeschlagenen Workflows | ✅ | - |
| `job_name` | Name des fehlgeschlagenen Jobs | ✅ | - |
| `failure_reason` | Grund für den Fehler | ❌ | 'Unknown failure' |
| `severity` | Schweregrad (low, medium, high, critical) | ❌ | 'medium' |
| `slack_webhook_url` | Slack Webhook URL | ❌ | - |
| `teams_webhook_url` | Microsoft Teams Webhook URL | ❌ | - |
| `github_token` | GitHub Token für Issue-Erstellung | ❌ | `${{ github.token }}` |
| `create_issue` | GitHub Issue erstellen | ❌ | 'true' |
| `notify_on_schedule` | Benachrichtigung bei geplanten Workflows | ❌ | 'true' |
| `notify_on_push` | Benachrichtigung bei Push-Events | ❌ | 'false' |
| `notify_on_pr` | Benachrichtigung bei PR-Events | ❌ | 'false' |

## 📤 Outputs

| Output | Beschreibung |
|--------|-------------|
| `notification_sent` | Ob Benachrichtigung erfolgreich gesendet wurde |
| `issue_created` | Ob GitHub Issue erstellt wurde |
| `issue_number` | Nummer des erstellten GitHub Issues |

## 🚀 Usage

### Basis-Verwendung

```yaml
- name: 📢 Notify on failure
  if: failure()
  uses: ./.github/actions/notify-failure
  with:
    workflow_name: ${{ github.workflow }}
    job_name: ${{ github.job }}
    failure_reason: "Tests failed with exit code 1"
    severity: "high"
    slack_webhook_url: ${{ secrets.SLACK_WEBHOOK_URL }}
```

### Erweiterte Konfiguration

```yaml
- name: 📢 Notify on critical failure
  if: failure()
  uses: ./.github/actions/notify-failure
  with:
    workflow_name: ${{ github.workflow }}
    job_name: ${{ github.job }}
    failure_reason: ${{ steps.previous_step.outputs.error_message }}
    severity: "critical"
    slack_webhook_url: ${{ secrets.SLACK_WEBHOOK_URL }}
    teams_webhook_url: ${{ secrets.TEAMS_WEBHOOK_URL }}
    create_issue: "true"
    notify_on_schedule: "true"
    notify_on_push: "true"
    notify_on_pr: "false"
```

### Conditional Notifications

```yaml
- name: 📢 Notify on production failure
  if: failure() && github.ref == 'refs/heads/main'
  uses: ./.github/actions/notify-failure
  with:
    workflow_name: ${{ github.workflow }}
    job_name: ${{ github.job }}
    severity: "critical"
    slack_webhook_url: ${{ secrets.SLACK_WEBHOOK_URL }}
    notify_on_push: "true"
```

## 🔧 Setup

### 1. Slack Webhook einrichten

1. Gehe zu [Slack Apps](https://api.slack.com/apps)
2. Erstelle eine neue App oder wähle eine bestehende
3. Aktiviere "Incoming Webhooks"
4. Erstelle einen neuen Webhook für deinen Channel
5. Füge die Webhook URL als Secret `SLACK_WEBHOOK_URL` hinzu

### 2. Microsoft Teams Webhook einrichten

1. Gehe zu deinem Teams Channel
2. Klicke auf "..." → "Connectors"
3. Suche nach "Incoming Webhook" und konfiguriere ihn
4. Kopiere die Webhook URL
5. Füge die URL als Secret `TEAMS_WEBHOOK_URL` hinzu

### 3. GitHub Secrets konfigurieren

```bash
# Repository Secrets hinzufügen
gh secret set SLACK_WEBHOOK_URL --body "https://hooks.slack.com/services/..."
gh secret set TEAMS_WEBHOOK_URL --body "https://outlook.office.com/webhook/..."
```

## 🎨 Notification Formats

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
        }
      ]
    }
  ]
}
```

## 🔍 Severity Levels

| Severity | Emoji | Color | Behavior |
|----------|-------|-------|----------|
| `critical` | 🚨 | Red | Immer benachrichtigen + Issue erstellen |
| `high` | 🔥 | Orange | Benachrichtigen + Issue erstellen |
| `medium` | ⚠️ | Yellow | Conditional benachrichtigen + Issue erstellen |
| `low` | ℹ️ | Blue | Conditional benachrichtigen, kein Issue |

## 🔄 Event-basierte Filterung

Die Action benachrichtigt intelligent basierend auf dem Event-Typ:

- **Schedule**: Standardmäßig aktiviert (`notify_on_schedule: true`)
- **Push**: Standardmäßig deaktiviert (`notify_on_push: false`)
- **Pull Request**: Standardmäßig deaktiviert (`notify_on_pr: false`)
- **Workflow Dispatch**: Immer aktiviert
- **Critical Severity**: Überschreibt alle Filter

## 🧪 Testing

```yaml
# Test der Notification Action
- name: 🧪 Test notification
  uses: ./.github/actions/notify-failure
  with:
    workflow_name: "Test Workflow"
    job_name: "Test Job"
    failure_reason: "This is a test notification"
    severity: "low"
    slack_webhook_url: ${{ secrets.SLACK_WEBHOOK_URL }}
    create_issue: "false"
```

## 🔒 Security

- Webhook URLs werden als GitHub Secrets gespeichert
- Keine sensiblen Daten in Nachrichten
- GitHub Token mit minimalen Berechtigungen
- Automatische Cleanup von temporären Dateien

## 🤝 Contributing

1. Teste Änderungen lokal mit `act`
2. Validiere Webhook-Formate
3. Dokumentiere neue Features
4. Erstelle Tests für neue Funktionalität

## 📝 Changelog

### v1.0.0
- Initial release
- Slack und Teams Support
- GitHub Issue Integration
- Severity-basierte Filterung
- Event-basierte Conditional Notifications
