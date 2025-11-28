"""
Time Series Analysis Agent - Orchestrator for production quality analysis.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json

from .base_agent import BaseAgent
from ..models import (
    ProductionStatistics,
    QualityInsight,
    AgentMessage,
)


class TimeSeriesAnalysisAgent(BaseAgent):
    """
    Primary agent that analyzes time series production data and coordinates
    with other agents to generate comprehensive quality insights.
    """

    def __init__(
        self,
        agent_id: str = "time_series_agent",
        name: str = "Time Series Analysis Agent",
        llm_client=None,
    ):
        """
        Initialize the Time Series Analysis Agent.

        Args:
            agent_id: Unique identifier for this agent
            name: Human-readable name
            llm_client: LLM client for analysis (should have a generate method)
        """
        super().__init__(agent_id, name)
        self.llm_client = llm_client
        self.agent_registry: Optional[Dict[str, BaseAgent]] = None

    def set_agent_registry(self, registry: Dict[str, BaseAgent]):
        """Set the agent registry for inter-agent communication."""
        self.agent_registry = registry

    def process(
        self,
        time_series_data: List[ProductionStatistics],
        time_period: Optional[str] = None,
    ) -> List[QualityInsight]:
        """
        Analyze time series production data and generate insights.

        Args:
            time_series_data: List of daily production statistics
            time_period: Optional description of the time period

        Returns:
            List of quality insights
        """
        if not time_series_data:
            return []

        # Prepare data for LLM analysis
        analysis_prompt = self._prepare_analysis_prompt(
            time_series_data, time_period
        )

        # Get initial analysis from LLM
        llm_response = self._analyze_with_llm(analysis_prompt)

        # Check if LLM wants to see images
        if self._should_request_images(llm_response):
            # Request images from Image Retrieval Agent
            image_insights = self._request_image_analysis(llm_response)
            # Re-analyze with image context
            llm_response = self._analyze_with_images(
                llm_response, image_insights
            )

        # Generate final insights
        insights = self._generate_insights(llm_response, time_series_data)

        return insights

    def _prepare_analysis_prompt(
        self,
        time_series_data: List[ProductionStatistics],
        time_period: Optional[str],
    ) -> str:
        """Prepare the prompt for LLM analysis."""
        # Convert statistics to JSON for LLM
        data_summary = []
        for stats in time_series_data:
            data_summary.append({
                "date": stats.date.isoformat(),
                "object_count": stats.object_count,
                "defect_count": stats.defect_count,
                "defect_rate": (
                    stats.defect_count / stats.object_count
                    if stats.object_count > 0
                    else 0
                ),
                "average_size": stats.average_size,
                "throughput_per_hour": stats.throughput_per_hour,
                "defect_types": {
                    k.value: v for k, v in stats.defect_types.items()
                },
                "color_distribution": stats.color_distribution,
            })

        period_desc = time_period or f"{len(time_series_data)} days"

        prompt = f"""You are analyzing production quality data for a manufacturing line.

Time Period: {period_desc}
Production Line: {time_series_data[0].production_line_id if time_series_data else "Unknown"}

Daily Production Statistics:
{json.dumps(data_summary, indent=2)}

Please analyze this time series data and identify:
1. Notable trends (improving/declining quality, throughput changes)
2. Anomalies or unusual patterns
3. Potential quality issues
4. Areas that might benefit from visual inspection

For each noteworthy finding, indicate:
- What you observed
- Why it's significant
- Whether you need to see images from specific time periods to investigate further
- If images are needed, specify the timestamp(s) and reason

Respond in JSON format with this structure:
{{
    "summary": "Overall assessment",
    "findings": [
        {{
            "type": "trend|anomaly|issue|pattern",
            "description": "...",
            "significance": "...",
            "needs_images": true/false,
            "image_timestamps": ["2024-01-15T14:30:00", ...],
            "image_reason": "Why images are needed"
        }}
    ],
    "recommendations": ["action 1", "action 2", ...]
}}
"""

        return prompt

    def _analyze_with_llm(self, prompt: str) -> Dict[str, Any]:
        """Analyze data using LLM."""
        if self.llm_client is None:
            # Fallback to mock response for testing
            return {
                "summary": "Mock analysis - LLM client not configured",
                "findings": [],
                "recommendations": [],
            }

        try:
            response = self.llm_client.generate(prompt)
            # Parse JSON response
            if isinstance(response, str):
                # Try to extract JSON from response
                import re
                json_match = re.search(r"\{.*\}", response, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
                return json.loads(response)
            return response
        except Exception as e:
            # Fallback response on error
            return {
                "summary": f"Analysis error: {str(e)}",
                "findings": [],
                "recommendations": [],
            }

    def _should_request_images(self, llm_response: Dict[str, Any]) -> bool:
        """Check if LLM response indicates need for images."""
        findings = llm_response.get("findings", [])
        return any(
            finding.get("needs_images", False) for finding in findings
        )

    def _request_image_analysis(
        self, llm_response: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Request image analysis from Image Retrieval Agent."""
        if not self.agent_registry:
            return []

        findings = llm_response.get("findings", [])
        image_insights = []

        for finding in findings:
            if not finding.get("needs_images", False):
                continue

            timestamps = finding.get("image_timestamps", [])
            reason = finding.get("image_reason", "Investigation requested")

            for timestamp in timestamps:
                try:
                    # Send request to Image Retrieval Agent
                    response = self.send_message(
                        to_agent="image_retrieval_agent",
                        request_type="get_images",
                        payload={
                            "timestamp": timestamp,
                            "time_range_minutes": 5,  # ±5 minutes
                            "reason": reason,
                            "context": finding,
                        },
                        agent_registry=self.agent_registry,
                    )
                    image_insights.append(response)
                except Exception as e:
                    # Log error but continue
                    print(f"Error requesting images for {timestamp}: {e}")

        return image_insights

    def _analyze_with_images(
        self, initial_response: Dict[str, Any], image_insights: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Re-analyze with image context."""
        if not image_insights:
            return initial_response

        prompt = f"""You previously analyzed production data and requested images for deeper investigation.

Initial Analysis:
{json.dumps(initial_response, indent=2)}

Image Analysis Results:
{json.dumps(image_insights, indent=2)}

Please provide an updated analysis incorporating the visual evidence from the images.
Update your findings, recommendations, and confidence levels based on what you see in the images.

Respond in the same JSON format as before.
"""

        return self._analyze_with_llm(prompt)

    def _generate_insights(
        self,
        llm_response: Dict[str, Any],
        time_series_data: List[ProductionStatistics],
    ) -> List[QualityInsight]:
        """Convert LLM response to QualityInsight objects."""
        insights = []
        findings = llm_response.get("findings", [])

        for finding in findings:
            # Determine severity based on finding type
            severity = self._determine_severity(finding)

            insight = QualityInsight(
                insight_type=finding.get("type", "unknown"),
                severity=severity,
                title=finding.get("description", "Quality Finding")[:100],
                description=finding.get("description", ""),
                timestamp=datetime.now(),
                production_line_id=(
                    time_series_data[0].production_line_id
                    if time_series_data
                    else "unknown"
                ),
                supporting_data=finding,
                recommended_actions=llm_response.get("recommendations", []),
                confidence=0.8,  # Could be extracted from LLM response
            )
            insights.append(insight)

        return insights

    def _determine_severity(self, finding: Dict[str, Any]) -> str:
        """Determine severity level from finding."""
        finding_type = finding.get("type", "").lower()
        description = finding.get("description", "").lower()

        if "critical" in description or "severe" in description:
            return "critical"
        elif "major" in description or "significant" in description:
            return "high"
        elif "minor" in description or "slight" in description:
            return "low"
        elif finding_type == "anomaly":
            return "medium"
        else:
            return "medium"
