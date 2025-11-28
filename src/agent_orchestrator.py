"""
Orchestrator for managing multiple agents and their interactions.
"""

from typing import Dict, List, Optional
from datetime import datetime

from .agents import BaseAgent, TimeSeriesAnalysisAgent, ImageRetrievalAgent
from .models import ProductionStatistics, QualityInsight


class AgentOrchestrator:
    """
    Orchestrator that manages agent lifecycle and coordinates interactions.
    """

    def __init__(
        self,
        llm_client=None,
        image_storage=None,
    ):
        """
        Initialize the orchestrator.

        Args:
            llm_client: LLM client for agent reasoning
            image_storage: Storage interface for images
        """
        self.agents: Dict[str, BaseAgent] = {}
        self.llm_client = llm_client
        self.image_storage = image_storage

        # Initialize agents
        self._initialize_agents()

    def _initialize_agents(self):
        """Initialize all agents in the system."""
        # Time Series Analysis Agent
        time_series_agent = TimeSeriesAnalysisAgent(
            llm_client=self.llm_client
        )
        self.agents[time_series_agent.agent_id] = time_series_agent

        # Image Retrieval Agent
        image_agent = ImageRetrievalAgent(
            image_storage=self.image_storage,
            llm_client=self.llm_client,
        )
        self.agents[image_agent.agent_id] = image_agent

        # Set agent registry for inter-agent communication
        for agent in self.agents.values():
            if hasattr(agent, "set_agent_registry"):
                agent.set_agent_registry(self.agents)

    def analyze_production_quality(
        self,
        time_series_data: List[ProductionStatistics],
        time_period: Optional[str] = None,
    ) -> List[QualityInsight]:
        """
        Analyze production quality data using the multi-agent system.

        Args:
            time_series_data: List of daily production statistics
            time_period: Optional description of the time period

        Returns:
            List of quality insights
        """
        time_series_agent = self.agents.get("time_series_agent")
        if not time_series_agent:
            raise ValueError("Time Series Analysis Agent not found")

        insights = time_series_agent.process(
            time_series_data=time_series_data,
            time_period=time_period,
        )

        return insights

    def get_agent(self, agent_id: str) -> Optional[BaseAgent]:
        """Get an agent by ID."""
        return self.agents.get(agent_id)

    def list_agents(self) -> List[str]:
        """List all agent IDs."""
        return list(self.agents.keys())
