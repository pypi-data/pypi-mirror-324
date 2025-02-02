import socket
from datetime import datetime
from typing import Optional
import requests
from uuid import uuid4
import urllib3
import json

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from aztp_client_py.common.config import ClientConfig
from aztp_client_py.common.types import (
    Identity,
    SecuredAgent,
    IssueIdentityRequest,
    Metadata,
)


class AztpClient:
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

    async def secureConnect(self, crew_agent: Optional[object] = None, name: str = None) -> SecuredAgent:
        """Create a secure connection for a workload.
        
        Args:
            crew_agent: Optional object representing the crew agent
            name: Name of the workload
            
        Returns:
            SecuredAgent: The secured agent with identity information
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
                # Convert response keys from camelCase
                identity = Identity(
                    spiffe_id=identity_info.get("spiffeId"),
                    certificate="",  # These will be fetched in get_identity
                    private_key="",
                    ca_certificate=""
                )
                
                return SecuredAgent(
                    name=name,
                    identity=identity,
                    metadata=metadata,
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

    async def get_identity(self, agent: SecuredAgent) -> Optional[Identity]:
        """Get the identity details for a secured agent."""
        if not agent.identity:
            return None
            
        # Extract just the workload name from the SPIFFE ID
        workload_id = agent.name
            
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
            # Convert response keys from camelCase
            return Identity(
                spiffe_id=identity_info.get("spiffeId"),
                certificate="",
                private_key="",
                ca_certificate=""
            )
        else:
            raise Exception("Invalid response format: missing 'data' field") 