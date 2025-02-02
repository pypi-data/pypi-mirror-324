# AZTP Client Python

AZTP (Agentic Zero Trust Protocol) Client is an enterprise-grade identity service client that provides secure workload identity management using SPIFFE (Secure Production Identity Framework for Everyone) standards. The client library facilitates secure communication between workloads by managing digital identities and certificates.

## Installation

```bash
pip install aztp-client
```

## Quick Start

```python
from aztp_client import Aztp

# Initialize client
client = Aztp(api_key="your-api-key")

# Create a secure agent
agent = await client.secure_connect(name="service1")

# Verify identity
is_valid = await client.verify_identity(agent)

# Get identity details
identity = await client.get_identity(agent)
```

## Features

- Workload Identity Management using SPIFFE standards
- Certificate Management (X.509)
- Secure Communication
- Identity Verification
- Metadata Management
- Environment-specific Configuration

## Configuration

The client can be configured using environment variables:

```bash
AZTP_API_KEY=your-api-key
AZTP_BASE_URL=https://api.aztp.yourdomain.com
AZTP_ENVIRONMENT=production
```

Or programmatically:

```python
client = AztpClient(
    api_key="your-api-key",
    base_url="https://api.aztp.yourdomain.com",
    environment="production"
)
```

## Documentation

For detailed documentation, please visit [docs.aztp.ai](https://docs.aztp.ai).

## License

MIT License 