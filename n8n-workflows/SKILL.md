---
name: n8n-workflows
description: >
  Design, build, and debug n8n automation workflows. Produces ready-to-import
  workflow JSON, node chains, and expressions. Use when the user mentions "n8n",
  "automation workflow", "automate X", "webhook to Y", "connect A to B",
  "scheduled job", "no-code automation", "Zapier alternative", "trigger →
  action", "sync tool to tool", or wants to automate social posting, email,
  data sync, notifications, or recurring tasks. Covers triggers, nodes,
  expressions, credentials, error handling, and self-hosted vs cloud.
argument-hint: "[trigger] → [action]"
metadata:
  author: jeaxes
  version: "1.0.0"
---

# n8n Workflows

You help the user design, build, and debug n8n automations. n8n chains **nodes**:
a trigger node starts the run, action nodes do the work, data flows node-to-node
as JSON items. Output is a workflow the user can paste into n8n (Import from
Clipboard) or build node by node.

## Before building

Ask for only what you cannot infer:
1. **Trigger** — what starts it? (Webhook, Schedule/Cron, app event, manual.)
2. **Steps** — what should happen, in order?
3. **Services** — which apps/APIs? (Gmail, HTTP, Google Sheets, Discord, Notion…)
4. **Self-hosted or n8n Cloud?** — affects available nodes and credential setup.

If the user is vague, propose the simplest working version and refine.

## How to deliver a workflow

Give, in this order:
1. **Plain-language flow:** `Trigger → Node1 → Node2 → …` with one line each.
2. **Node details:** for each node, its type, key parameters, and any expression.
3. **Import JSON:** a valid n8n workflow export in a code block (see template).
4. **Setup steps:** which credentials to create, where to paste the webhook URL, how to test.

## Core node patterns

- **Webhook trigger:** gives a URL; external service POSTs to it. Use for "when X happens elsewhere".
- **Schedule trigger:** cron-based. Use for "every day at 9", "hourly", recurring jobs.
- **HTTP Request:** call any REST API when no dedicated node exists.
- **IF / Switch:** branch on a condition.
- **Set / Edit Fields:** shape the JSON (rename, add, drop fields).
- **Code node:** JavaScript for logic the built-in nodes can't express.
- **Merge:** join two branches.
- **No-Op / Respond to Webhook:** return a response to the caller.

## Expressions

n8n expressions use `{{ }}` and reference prior node data:
- Current item field: `{{ $json.fieldName }}`
- Named node output: `{{ $node["Webhook"].json.body.email }}`
- Now / dates: `{{ $now }}`, `{{ $now.plus({days:1}) }}`
- Env/credentials are configured in the UI, never hard-coded in JSON.

## Common automations (ready to adapt)

| Goal | Chain |
|---|---|
| Post to social on schedule | Schedule → (optional AI text) → HTTP/Platform node |
| Form/webhook → email | Webhook → Set → Gmail/SMTP → Respond to Webhook |
| Daily report | Schedule → data source → format → Discord/Slack/Email |
| Sync new rows | Schedule → Sheets/DB read → IF (new?) → target app |
| Lead to CRM | Webhook → validate (IF) → CRM node → notify |

## Import JSON template

```json
{
  "name": "Example: Webhook to Email",
  "nodes": [
    {
      "parameters": { "httpMethod": "POST", "path": "lead" },
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 2,
      "position": [250, 300]
    },
    {
      "parameters": {
        "sendTo": "={{ $json.body.email }}",
        "subject": "Danke für deine Anfrage",
        "message": "Wir melden uns."
      },
      "name": "Send Email",
      "type": "n8n-nodes-base.gmail",
      "typeVersion": 2,
      "position": [500, 300]
    }
  ],
  "connections": {
    "Webhook": { "main": [[{ "node": "Send Email", "type": "main", "index": 0 }]] }
  }
}
```
Node `type`/`typeVersion` and credential references must match the user's n8n
version — tell them to re-select the credential after import.

## Reliability

- Add error handling: set nodes to "Continue on Fail" where a step may error,
  or add an **Error Trigger** workflow for alerts.
- Test with the **Execute Workflow** button and pinned sample data before activating.
- Never put API keys or secrets in the workflow JSON — use n8n Credentials.
- For self-hosted: confirm the node/package is installed; some nodes are community nodes.

## Scope

Build and debug workflows and expressions. Do not invent node types that don't
exist — if unsure whether a dedicated node exists, use an HTTP Request node and say so.
