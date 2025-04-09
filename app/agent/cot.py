from typing import Optional

from pydantic import Field

from ..agent.base import BaseAgent
from ..llm import LLM
from ..logger import logger
from ..prompt.cot import NEXT_STEP_PROMPT, SYSTEM_PROMPT
from ..schema import AgentState, Message


class CoTAgent(BaseAgent):
    """Chain of Thought Agent - Focuses on demonstrating the thinking process of large language models without executing tools"""

    name: str = "cot"
    description: str = "An agent that uses Chain of Thought reasoning"

    system_prompt: str = SYSTEM_PROMPT
    next_step_prompt: Optional[str] = NEXT_STEP_PROMPT

    llm: LLM = Field(default_factory=LLM)

    max_steps: int = 1  # CoT typically only needs one step to complete reasoning

    async def step(self, session_id: str = "default") -> str:
        """Execute one step of chain of thought reasoning"""
        logger.info(f"🧠 {self.name} is thinking...")
        session_messages = self.memory.get_session_messages(session_id)

        # If next_step_prompt exists and this isn't the first message, add it to user messages
        if self.next_step_prompt and len(session_messages) > 1:
            self.memory.add_message(Message.user_message(self.next_step_prompt))

        # Use system prompt and user messages
        response = await self.llm.ask(
            messages=session_messages,
            system_msgs=[Message.system_message(self.system_prompt)]
            if self.system_prompt
            else None,
        )

        # Record assistant's response
        self.memory.add_message(Message.assistant_message(response), session_id=session_id)

        # Set state to finished after completion
        self.state = AgentState.FINISHED

        return response
