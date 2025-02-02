import socket
from datetime import datetime
from typing import Optional
import requests
from uuid import uuid4

from aztp_client.common.config import ClientConfig
from aztp_client.common.types import (
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
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        })

    async def secure_connect(self, name: str) -> SecuredAgent:
        """Create a secure connection for a workload."""
        metadata = Metadata(
            hostname=socket.gethostname(),
            environment=self.config.environment,
        )
        
        request = IssueIdentityRequest(
            workload_id=str(uuid4()),
            agent_id=name,
            timestamp=datetime.utcnow(),
            method="secure_connect",
            metadata=metadata,
        )
        
        response = self.session.post(
            f"{self.config.base_url}/aztp/issue-identity",
            json=request.model_dump(),
            timeout=self.config.timeout,
        )
        response.raise_for_status()
        
        identity_data = response.json()
        identity = Identity(**identity_data)
        
        return SecuredAgent(
            name=name,
            identity=identity,
            metadata=metadata,
        )

    async def verify_identity(self, agent: SecuredAgent) -> bool:
        """Verify the identity of a secured agent."""
        if not agent.identity:
            return False
            
        response = self.session.post(
            f"{self.config.base_url}/aztp/verify-identity",
            json={"spiffe_id": agent.identity.spiffe_id},
            timeout=self.config.timeout,
        )
        response.raise_for_status()
        
        result = response.json()
        return result.get("valid", False)

    async def get_identity(self, agent: SecuredAgent) -> Optional[Identity]:
        """Get the identity details for a secured agent."""
        if not agent.identity:
            return None
            
        response = self.session.get(
            f"{self.config.base_url}/aztp/get-identity/{agent.identity.spiffe_id}",
            timeout=self.config.timeout,
        )
        response.raise_for_status()
        
        identity_data = response.json()
        return Identity(**identity_data) 