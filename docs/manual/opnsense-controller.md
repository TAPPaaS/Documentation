---
title: OPNsense Controller
description: CLI tools for managing OPNsense firewall, VLANs, DHCP, and DNS
---

# OPNsense Controller

The OPNsense Controller is a CLI tool suite for managing firewalls, VLANs, DHCP, and DNS configurations.

## Core Capabilities

The package provides four primary command-line utilities:

- **Main controller** - Handles VLAN, DHCP, and firewall management through a unified interface
- **Firewall manager** - Dedicated firewall rule manager
- **DNS manager** - DNS host entry handler
- **Zone manager** - Zone configuration system that reads from JSON specifications

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

