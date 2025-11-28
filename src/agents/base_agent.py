"""
Base agent class for the multi-agent system.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime
import uuid

from ..models import AgentMessage


class BaseAgent(ABC):
    """Base class for all agents in the system."""

    def __init__(self, agent_id: str, name: str):
        """
        Initialize the base agent.

        Args:
            agent_id: Unique identifier for this agent
            name: Human-readable name for this agent
        """
        self.agent_id = agent_id
        self.name = name
        self.message_handlers: Dict[str, callable] = {}

    def register_handler(self, request_type: str, handler: callable):
        """
        Register a message handler for a specific request type.

        Args:
            request_type: Type of request to handle
            handler: Function to handle the request
        """
        self.message_handlers[request_type] = handler

    def handle_message(self, message: AgentMessage) -> Dict[str, Any]:
        """
        Handle an incoming message from another agent.

        Args:
            message: The message to handle

        Returns:
            Response dictionary
        """
        if message.to_agent != self.agent_id:
            raise ValueError(
                f"Message intended for {message.to_agent}, "
                f"but received by {self.agent_id}"
            )

        handler = self.message_handlers.get(message.request_type)
        if not handler:
            raise ValueError(
                f"No handler registered for request type: {message.request_type}"
            )

        return handler(message.payload)

    def send_message(
        self,
        to_agent: str,
        request_type: str,
        payload: Dict[str, Any],
        agent_registry: Optional[Dict[str, "BaseAgent"]] = None,
    ) -> Dict[str, Any]:
        """
        Send a message to another agent.

        Args:
            to_agent: ID of the target agent
            request_type: Type of request
            payload: Message payload
            agent_registry: Registry of available agents

        Returns:
            Response from the target agent
        """
        if agent_registry is None:
            raise ValueError("Agent registry required to send messages")

        if to_agent not in agent_registry:
            raise ValueError(f"Agent {to_agent} not found in registry")

        message = AgentMessage(
            from_agent=self.agent_id,
            to_agent=to_agent,
            request_type=request_type,
            payload=payload,
            timestamp=datetime.now(),
            correlation_id=str(uuid.uuid4()),
        )

        target_agent = agent_registry[to_agent]
        return target_agent.handle_message(message)

    @abstractmethod
    def process(self, input_data: Any) -> Any:
        """
        Main processing method for the agent.

        Args:
            input_data: Input data to process

        Returns:
            Processing result
        """
        pass
