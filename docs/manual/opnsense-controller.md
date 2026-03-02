---
title: OPNsense Controller
description: CLI tools for managing OPNsense firewall, VLANs, DHCP, DNS, and Caddy reverse proxy
---

# OPNsense Controller

The OPNsense Controller is a CLI tool suite for managing firewalls, VLANs, DHCP, DNS, and Caddy reverse proxy configurations.

## Core Capabilities

The package provides five command-line utilities:

| Command | Description |
|---------|-------------|
| `opnsense-controller` | Main CLI with examples for VLANs, DHCP, and firewall management |
| `opnsense-firewall` | Standalone firewall rule management (create, list, delete rules) |
| `dns-manager` | DNS host entry management for Dnsmasq |
| `zone-manager` | Automated zone configuration from zones.json |
| `caddy-manager` | Caddy reverse proxy domain and handler management |

## Getting Started

### Installation

Installation requires Nix and an OPNsense instance with API access enabled.

### API Credentials

Create credentials in the OPNsense web interface:

1. Go to **System > Access > Users**
2. Generate an API key

The controller expects credentials in `~/.opnsense-credentials.txt`:
```
<api-token>
<api-secret>
```

The system automatically detects API ports by probing ports 443 and 8443 sequentially, supporting various OPNsense deployment configurations.

## Configuration

### Credential File (Recommended)

```bash
cat > ~/.opnsense-credentials.txt <<EOF
your-api-token
your-api-secret
EOF
chmod 600 ~/.opnsense-credentials.txt
```

### Environment Variables

Environment variables allow runtime customization:

- `OPNSENSE_TOKEN` - API token
- `OPNSENSE_SECRET` - API secret
- Hostname, port, SSL verification, timeout values, and retry counts

## CLI Tools

### Main Controller

The primary tool supports three operational modes:

- **VLAN management**
- **DHCP configuration**
- **Firewall rules**

The `--execute` flag enables actual changes; dry-run mode is default.

### Firewall Manager

The dedicated firewall CLI enables rule creation with comprehensive filtering options:

- Source/destination networks
- Ports and protocols
- Actions (allow, block, reject)
- Logging and priority sequencing
- Batch operations with deferred application

### Zone Manager

Automates configuration from `zones.json` definitions:

- Manages VLANs
- Configures DHCP ranges
- Creates firewall rules according to zone specifications
- Supports selective configuration of individual components
- Provides programmatic access for scripting

---

## DNS Manager

The DNS Manager is a dedicated command-line tool for managing DNS host entries in OPNsense's Dnsmasq service.

### Installation

The DNS manager is installed as part of the OPNsense controller Nix package:

```bash
# Build the OPNsense controller package
cd ~/TAPPaaS/src/foundation/tappaas-cicd/opnsense-controller
nix-build -A default default.nix

# The dns-manager command will be available in the result
./result/bin/dns-manager --help
```

### Commands

| Command | Arguments | Description |
|---------|-----------|-------------|
| `add` | `<hostname> <domain> <ip>` | Add or update a DNS host entry |
| `delete` | `<hostname> <domain>` | Delete a DNS host entry by hostname and domain |
| `list` | - | List all DNS host entries |

### Usage Examples

**Add a DNS Entry:**
```bash
dns-manager --no-ssl-verify add backup mgmt.internal 10.0.0.12
```

With custom description:
```bash
dns-manager --no-ssl-verify add backup mgmt.internal 10.0.0.12 --description "PBS Backup Server"
```

**Delete a DNS Entry:**
```bash
dns-manager --no-ssl-verify delete backup mgmt.internal
```

**List DNS Entries:**
```bash
dns-manager --no-ssl-verify list
```

**Dry-Run Mode:**
```bash
dns-manager --no-ssl-verify --check-mode add backup mgmt.internal 10.0.0.12
```

### Options

| Option | Description |
|--------|-------------|
| `--firewall HOST` | Firewall IP/hostname (default: firewall.mgmt.internal) |
| `--credential-file PATH` | Path to credential file (default: ~/.opnsense-credentials.txt) |
| `--no-ssl-verify` | Disable SSL certificate verification |
| `--debug` | Enable debug logging |
| `--check-mode` | Dry-run mode (don't make actual changes) |

### Authentication

The DNS manager uses the same credentials as other OPNsense controller tools:

1. **Credential file** (recommended):
   ```bash
   cat > ~/.opnsense-credentials.txt <<EOF
   your-api-token
   your-api-secret
   EOF
   chmod 600 ~/.opnsense-credentials.txt
   ```

2. **Environment variables**:
   ```bash
   export OPNSENSE_TOKEN="your-api-token"
   export OPNSENSE_SECRET="your-api-secret"
   ```

3. **Command-line option**:
   ```bash
   dns-manager --credential-file /path/to/creds.txt ...
   ```

### Integration with TAPPaaS

The DNS manager is automatically used by module configuration scripts:

```bash
# Example from PBS backup configuration
dns-manager --no-ssl-verify add backup mgmt.internal ${PBS_NODE_IP} --description "PBS Backup Server"
```

### Technical Details

- Uses OPNsense's Dnsmasq DHCP/DNS service
- Creates static host entries that work for both DNS resolution and DHCP reservations
- Manages entries via the OPNsense API
- Implemented as a Python module in `opnsense_controller.dns_manager_cli`

---

## Caddy Manager

The Caddy Manager provides a dedicated CLI for managing Caddy reverse proxy domains and handlers on OPNsense. It is used by the `firewall:proxy` service scripts to automate proxy setup for TAPPaaS modules.

### Commands

| Command | Description |
|---------|-------------|
| `add-domain <domain>` | Add a reverse proxy domain |
| `add-handler <domain>` | Add a reverse proxy handler for a domain |
| `delete-domain <domain>` | Delete a reverse proxy domain |
| `delete-handler` | Delete a handler by `--description` or `--uuid` |
| `list` | List all domains and handlers |
| `reconfigure` | Reconfigure Caddy (apply pending changes) |

### Usage Examples

**List all reverse proxy domains and handlers:**
```bash
caddy-manager list --no-ssl-verify
```

**Add a domain (Caddy will obtain a TLS certificate for it):**
```bash
caddy-manager add-domain app.test.tappaas.org --description "TAPPaaS: myapp" --no-ssl-verify
```

**Add a handler that routes traffic to an upstream VM:**
```bash
caddy-manager add-handler app.test.tappaas.org \
    --upstream myapp.srv.internal \
    --port 8080 \
    --description "TAPPaaS: myapp" \
    --no-ssl-verify
```

**Delete a handler by description:**
```bash
caddy-manager delete-handler --description "TAPPaaS: myapp" --no-ssl-verify
```

**Delete a domain:**
```bash
caddy-manager delete-domain app.test.tappaas.org --no-ssl-verify
```

**Reconfigure Caddy (regenerate Caddyfile and reload):**
```bash
caddy-manager reconfigure --no-ssl-verify
```

**Dry-run mode:**
```bash
caddy-manager add-domain app.test.tappaas.org --check-mode --no-ssl-verify
```

### Options

| Option | Description |
|--------|-------------|
| `--firewall HOST` | Firewall IP/hostname (default: firewall.mgmt.internal) |
| `--api-port PORT` | OPNsense API port (default: auto-detect by probing 443, then 8443) |
| `--credential-file PATH` | Path to credential file |
| `--no-ssl-verify` | Disable SSL certificate verification |
| `--debug` | Enable debug logging |
| `--check-mode` | Dry-run mode (don't make actual changes) |

### add-domain Options

| Option | Description |
|--------|-------------|
| `domain` | Domain FQDN, e.g., `app.test.tappaas.org` (positional, required) |
| `--description` | Description for the domain entry |

### add-handler Options

| Option | Description |
|--------|-------------|
| `domain` | Domain FQDN to attach the handler to (positional, required) |
| `--upstream` | Upstream server hostname, e.g., `app.srv.internal` (required) |
| `--port` | Upstream port (default: `80`) |
| `--description` | Description for the handler entry |

### delete-handler Options

| Option | Description |
|--------|-------------|
| `--description` | Handler description to match (mutually exclusive with `--uuid`) |
| `--uuid` | Handler UUID to delete directly (mutually exclusive with `--description`) |

### Integration with TAPPaaS

The Caddy manager is automatically used by the `firewall:proxy` service scripts:

```bash
# Typical module proxy setup (what install-service.sh does)
caddy-manager add-domain vaultwarden.test.tappaas.org \
    --description "TAPPaaS: vaultwarden" --no-ssl-verify
caddy-manager add-handler vaultwarden.test.tappaas.org \
    --upstream vaultwarden.srv.internal \
    --port 80 \
    --description "TAPPaaS: vaultwarden" --no-ssl-verify
caddy-manager reconfigure --no-ssl-verify

# Cleanup (what delete-service.sh does)
caddy-manager delete-handler --description "TAPPaaS: vaultwarden" --no-ssl-verify
caddy-manager delete-domain vaultwarden.test.tappaas.org --no-ssl-verify
caddy-manager reconfigure --no-ssl-verify
```

### Technical Details

- Manages Caddy reverse proxy through the OPNsense Caddy plugin API
- Handles automatic TLS certificate provisioning via ACME
- Creates domain entries and upstream handlers
- Implemented as a Python module in `opnsense_controller.caddy_cli`

---

## Programmatic Interface

Python developers can import manager classes directly for integration into automation workflows:

- Connection testing
- Specification retrieval
- Batch operations
- Rule enumeration and creation
- Toggle functionality

### DHCP Manager

Handles both dynamic ranges and static reservations with:

- Lease time configuration
- Domain configuration

### VLAN Management

Supports interface assignment through an optional custom PHP extension.

