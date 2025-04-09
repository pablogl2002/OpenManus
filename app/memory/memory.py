from ..schema import BaseMemory, Message
from typing import Dict, List
from pydantic import Field

class Memory(BaseMemory):
    sessions: Dict[str, List[Message]] = Field(default_factory=dict)
    max_messages: int = Field(default=100)

    def add_message(self, message: Message, session_id: str="default") -> None:
        """Add a message to memory"""
        messages = self.sessions.get(session_id, [])
        messages.append(message)

        # Optional: Implement message limit
        if len(self.sessions.get(session_id, [])) > self.max_messages:
            self.sessions[session_id] = messages[-self.max_messages :]
        else:
            self.sessions[session_id] = messages

    def add_messages(self, messages: List[Message], session_id: str="default") -> None:
        """Add multiple messages to memory"""
        messages = self.sessions.get(session_id, [])
        messages.extend(messages)
        self.sessions[session_id] = messages

    def clear(self, session_id: str="default") -> None:
        """Clear all messages"""
        messages = self.sessions.get(session_id, [])
        messages.clear()
        self.sessions[session_id] = messages

    def get_recent_messages(self, n: int, session_id: str="default") -> List[Message]:
        """Get n most recent messages"""
        return self.sessions[session_id][-n:]

    def get_session_messages(self, session_id: str="default") -> List[Message]:
        return self.sessions[session_id]

    def to_dict_list(self, session_id: str="default") -> List[dict]:
        """Convert messages to list of dicts"""
        messages = self.sessions.get(session_id, [])
        return [msg.to_dict() for msg in messages]
