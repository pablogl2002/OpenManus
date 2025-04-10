from ..schema import BaseMemory, Message
from libs.redis_adapter.main import RedisHandler
from pydantic import Field
from typing import List

import ast

from ..config import config

memory_config = config.memory_config
print("REDIS: ", memory_config)

class RedisMemory(BaseMemory):
    max_messages: int = Field(default=100)

    redis_handler: RedisHandler = RedisHandler(
        redis_broker=memory_config.config.host,
        redis_broker_port=memory_config.config.port,
        redis_db=memory_config.config.database,
        redis_pwd=memory_config.config.password,
    )

    def add_message(self, message: Message, session_id: str="default") -> None:
        """Add a message to memory"""
        old_messages = self.redis_handler.get(f"ai:messages:{session_id}")
        if old_messages:
            new_messages = ast.literal_eval(old_messages)
        else:
            new_messages = []

        new_messages.append(message.to_dict())
        # Optional: Implement message limit
        if len(new_messages) > self.max_messages:
            new_messages = new_messages[-self.max_messages :]

        self.redis_handler.set(f"ai:messages:{session_id}", str(new_messages))

    def add_messages(self, messages: List[Message], session_id: str="default") -> None:
        """Add multiple messages to memory all with the same session_id"""
        old_messages = self.redis_handler.get(f"ai:messages:{session_id}")
        if old_messages:
            new_messages = ast.literal_eval(old_messages)
        else:
            new_messages = []

        for message in messages:
            new_messages.append(message.to_dict())

        # Optional: Implement message limit
        if len(new_messages) > self.max_messages:
            new_messages = new_messages[-self.max_messages :]

        self.redis_handler.set(f"ai:messages:{session_id}", str(new_messages))

    def clear(self, session_id: str="default") -> None:
        """Clear all messages"""
        self.redis_handler.delete(f"ai:messages:{session_id}:*")

    def get_recent_messages(self, n: int, session_id: str="default") -> List[Message]:
        """Get n most recent messages"""
        messages = self.redis_handler.get(f"ai:messages:{session_id}")
        if messages:
            messages = ast.literal_eval(messages)
        else:
            messages = []

        return messages[-n:]

    def get_session_messages(self, session_id: str="default") -> List[Message]:
        messages = self.redis_handler.get(f"ai:messages:{session_id}")
        if messages:
            messages = ast.literal_eval(messages)
        else:
            messages = []

        return messages

    def to_dict_list(self, session_id: str="default") -> List[dict]:
        """Convert messages to list of dicts"""
        messages = self.redis_handler.get(f"ai:messages:{session_id}")
        if messages:
            messages = ast.literal_eval(messages)
        else:
            messages = []

        return messages
