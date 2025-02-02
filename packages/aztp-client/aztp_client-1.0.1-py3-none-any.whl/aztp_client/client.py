import socket
from datetime import datetime
from typing import Optional, Callable
import requests
from uuid import uuid4
import urllib3
import json
from dataclasses import dataclass

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from aztp_client.common.config import ClientConfig
from aztp_client.common.types import (
    Identity,
    SecuredAgent,
    IssueIdentityRequest,
    Metadata,
)

@dataclass
class SecureConnection:
    identity: Identity
    verify: Callable

class Aztp:
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        environment: Optional[str] = None,
        timeout: Optional[int] = None,
    ):
        """Initialize AZTP client with optional configuration."""
        self.config = ClientConfig.create(
            api_key=api_key,
            base_url=base_url,
            environment=environment,
            timeout=timeout,
        )
        self.session = requests.Session()
        self.session.headers.update({
            "api_access_key": f"{self.config.api_key}",
            "Content-Type": "application/json",
        })
        print(f"API Key: {self.config.api_key[:8]}...")

    def _get_url(self, endpoint: str) -> str:
        """Get full URL for an endpoint."""
        # Just join the base URL with the endpoint
        base_url = self.config.base_url.rstrip('/')
        endpoint = endpoint.lstrip('/')
        return f"{base_url}/{endpoint}"

    async def secure_connect(self, crew_agent: Optional[object] = None, name: str = None) -> SecureConnection:
        """Create a secure connection for a workload.
        
        Args:
            crew_agent: Optional object representing the crew agent
            name: Name of the workload
            
        Returns:
            SecureConnection: An object containing identity information and verify function
        """
        if name is None:
            raise ValueError("name parameter is required")
            
        metadata = Metadata(
            hostname=socket.gethostname(),
            environment=self.config.environment,
        )
        
        request = IssueIdentityRequest(
            workload_id=name,
            agent_id="aztp",
            timestamp=datetime.utcnow().isoformat(),
            method="node",
            metadata=metadata,
        )
        
        # Convert request to dict and ensure proper casing for JSON
        request_data = {
            "workloadId": request.workload_id,
            "agentId": request.agent_id,
            "timestamp": request.timestamp,
            "method": request.method,
            "metadata": {
                "hostname": request.metadata.hostname,
                "environment": request.metadata.environment,
                "extra": request.metadata.extra
            }
        }
        
        url = self._get_url("issue-identity")
        
        try:
            response = self.session.post(
                url,
                json=request_data,
                timeout=self.config.timeout,
                verify=False,  # Disable SSL verification
            )
            
            response.raise_for_status()
            
            identity_data = response.json()
            
            # Get the data field from the response
            if isinstance(identity_data, dict) and 'data' in identity_data:
                identity_info = identity_data['data']
                
                # Create identity object
                identity = Identity(
                    spiffe_id=identity_info.get("spiffeId"),
                    certificate="",
                    private_key="",
                    ca_certificate=""
                )
                
                # Create secured agent instance for verify function
                secured_agent = SecuredAgent(
                    name=name,
                    identity=identity,
                    metadata=metadata,
                )
                
                # Return SecureConnection instance
                return SecureConnection(
                    identity=identity,
                    verify=lambda: self.verify_identity(secured_agent)
                )
            else:
                raise Exception("Invalid response format: missing 'data' field")
        except requests.exceptions.RequestException as e:
            print(f"\nRequest failed: {str(e)}")
            if hasattr(e.response, 'text'):
                print(f"Error response: {e.response.text}")
            raise

    async def verify_identity(self, agent: SecuredAgent) -> bool:
        """Verify the identity of a secured agent."""
        if not agent.identity:
            return False
            
        response = self.session.post(
            self._get_url("verify-identity"),
            json={"spiffeId": agent.identity.spiffe_id},
            timeout=self.config.timeout,
            verify=False,  # Disable SSL verification
        )
        response.raise_for_status()
        
        result = response.json()
        if isinstance(result, dict) and 'data' in result:
            return result['data'].get("valid", False)
        return result.get("valid", False)

    async def get_identity(self, agent: SecureConnection) -> dict:
        """Get the identity details for a secured agent.
        
        Args:
            agent: The SecureConnection object to get identity for
            
        Returns:
            dict: The identity information including metadata and workload info
        """
        if not agent.identity:
            return None
            
        # Extract workload name from the SPIFFE ID
        workload_id = agent.identity.spiffe_id.split('/')[-1]
            
        response = self.session.get(
            self._get_url(f"get-identity/{workload_id}"),
            timeout=self.config.timeout,
            verify=False,  # Disable SSL verification
        )
        response.raise_for_status()
        
        identity_data = response.json()
        
        # Get the data field from the response
        if isinstance(identity_data, dict) and 'data' in identity_data:
            identity_info = identity_data['data']
            
            # Convert response to match required format
            return {
                "spiffeId": identity_info.get("spiffeId"),
                "createdAt": identity_info.get("createdAt"),
                "environment": identity_info.get("environment"),
                "issuedAt": identity_info.get("issuedAt"),
                "metadata": {
                    "hostname": identity_info.get("metadata", {}).get("hostname"),
                    "environment": identity_info.get("metadata", {}).get("environment")
                },
                "rotateAt": identity_info.get("rotateAt"),
                "selectors": [
                    f"workload:id:{workload_id}",
                    "agent:id:aztp",
                    "method:node",
                    f"metadata:hostname:{identity_info.get('metadata', {}).get('hostname')}",
                    f"metadata:environment:{identity_info.get('metadata', {}).get('environment')}"
                ],
                "status": identity_info.get("status", "active"),
                "updatedAt": identity_info.get("updatedAt"),
                "workloadInfo": {
                    "workloadId": workload_id,
                    "agentId": "aztp",
                    "method": "node",
                    "timestamp": identity_info.get("updatedAt"),
                    "hostname": identity_info.get("metadata", {}).get("hostname"),
                    "environment": identity_info.get("metadata", {}).get("environment"),
                    "additionalMetadata": {
                        "hostname": identity_info.get("metadata", {}).get("hostname"),
                        "environment": identity_info.get("metadata", {}).get("environment")
                    }
                }
            }
        else:
            raise Exception("Invalid response format: missing 'data' field") 