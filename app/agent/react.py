from abc import ABC, abstractmethod
from typing import Optional

from pydantic import Field

from ..agent.base import BaseAgent
from ..llm import LLM
from ..schema import AgentState
# , BaseMemory

class ReActAgent(BaseAgent, ABC):
    name: str
    description: Optional[str] = None

    system_prompt: Optional[str] = None
    next_step_prompt: Optional[str] = None

    llm: Optional[LLM] = Field(default_factory=LLM)
    # memory: BaseMemory = Field(default_factory=BaseMemory)
    state: AgentState = AgentState.IDLE

    max_steps: int = 10
    current_step: int = 0

    @abstractmethod
    async def think(self, session_id: str =  "default") -> bool:
        """Process current state and decide next action"""

    @abstractmethod
    async def act(self, session_id: str =  "default") -> str:
        """Execute decided actions"""

    async def step(self, session_id: str =  "default") -> str:
        """Execute a single step: think and act."""
        should_act = await self.think()
        if not should_act:
            return "Thinking complete - no action needed"
        return await self.act()
