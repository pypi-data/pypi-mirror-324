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
## Example

```python
import asyncio
import os
from aztp_client import Aztp
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def main():
    # Initialize the client with your API key
    client = Aztp(
        api_key=os.getenv("AZTP_API_KEY"),
    )

    try:
        crewAgent = {}
        
        # Create a secure agent
        print("\nCreating secure agent...")
        agent = await client.secure_connect(crewAgent, name="MyAgent") # you may edit the name to your liking
        print(f"Agent created successfully!")
        
        if agent.identity.spiffe_id:
            print(f"Agent: {agent.identity.spiffe_id}")

        
        # Verify the identity
        print("\nVerifying identity...")
        is_valid = await agent.verify()
        print(f"Identity valid: {is_valid}")

        
        # Get identity details
        print("\nGetting identity details...")
        identity = await client.get_identity(agent)
        if identity:
            print(f"Retrieved identity: {identity}")
        else:
            print("No identity found") 

    except ConnectionError as e:
        print(f"Connection Error: Could not connect to the AZTP server. Please check your connection and server URL.")
        print(f"Details: {e}")
    except Exception as e:
        print(f"Error: {str(e)}")
        print("\nCurrent configuration:")
        print(f"Base URL: {client.config.base_url}")
        print(f"Environment: {client.config.environment}")
        print("API Key: ********")  # Don't print the API key for security

if __name__ == "__main__":
    asyncio.run(main())
```

## Features

- Workload Identity Management using SPIFFE standards
- Certificate Management (X.509)
- Secure Communication
- Identity Verification
- Metadata Management
- Environment-specific Configuration

## License

MIT License 