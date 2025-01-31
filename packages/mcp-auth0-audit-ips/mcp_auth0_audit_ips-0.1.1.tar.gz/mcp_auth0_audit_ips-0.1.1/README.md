# MCP Auth0 Audit IPs

Audit IPs from Auth0 logs and send them to Tinybird.

## Prerequisites

- [Auth0 log](https://www.tinybird.co/docs/get-data-in/guides/ingest-auth0-logs) stream to Tinybird
- [Tinybird](https://www.tinybird.co/) account
- [VirusTotal](https://www.virustotal.com/) account
- [AbuseIPDB](https://www.abuseipdb.com/) account

## Install in Claude

Edit `claude_desktop_config.json` and add the following:

```bash
    "auth0_suspicious_ips": {
      "command": "uvx",
      "args": [
        "mcp-auth0-audit-ips"
      ],
      "env": {
        "TINYBIRD_TOKEN": "your_tinybird_token",
        "ABUSEIPDB_KEY": "your_abuseipdb_key",
        "VT_KEY": "your_virustotal_key",
        "TINYBIRD_HOST": "api.tinybird.co"
      }
    }
```
