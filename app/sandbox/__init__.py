"""
Docker Sandbox Module

Provides secure containerized execution environment with resource limits
and isolation for running untrusted code.
"""
from ..sandbox.client import (
    BaseSandboxClient,
    LocalSandboxClient,
    create_sandbox_client,
)
from ..sandbox.core.exceptions import (
    SandboxError,
    SandboxResourceError,
    SandboxTimeoutError
)
from ..sandbox.core.manager import SandboxManager
from ..sandbox.core.sandbox import DockerSandbox

# Create default sandbox client instance
SANDBOX_CLIENT = create_sandbox_client()

__all__ = [
    "DockerSandbox",
    "SandboxManager",
    "BaseSandboxClient",
    "LocalSandboxClient",
    "create_sandbox_client",
    "SandboxError",
    "SandboxTimeoutError",
    "SandboxResourceError",
    "SANDBOX_CLIENT",
]
