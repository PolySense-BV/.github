"""
Image Retrieval Agent - Fetches and analyzes production line images.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json

from .base_agent import BaseAgent
from ..models import ImageMetadata, AgentMessage


class ImageRetrievalAgent(BaseAgent):
    """
    Agent specialized in retrieving and analyzing production line images
    based on timestamps and criteria.
    """

    def __init__(
        self,
        agent_id: str = "image_retrieval_agent",
        name: str = "Image Retrieval Agent",
        image_storage=None,
        llm_client=None,
    ):
        """
        Initialize the Image Retrieval Agent.

        Args:
            agent_id: Unique identifier for this agent
            name: Human-readable name
            image_storage: Storage interface for images (should have get_images method)
            llm_client: LLM client for image analysis
        """
        super().__init__(agent_id, name)
        self.image_storage = image_storage
        self.llm_client = llm_client

        # Register message handlers
        self.register_handler("get_images", self._handle_get_images)

    def process(
        self,
        timestamp: datetime,
        time_range_minutes: int = 5,
        production_line_id: Optional[str] = None,
    ) -> List[ImageMetadata]:
        """
        Retrieve images around a specific timestamp.

        Args:
            timestamp: Target timestamp
            time_range_minutes: Time range in minutes (±)
            production_line_id: Optional filter by production line

        Returns:
            List of image metadata
        """
        if self.image_storage is None:
            # Return mock data for testing
            return self._get_mock_images(timestamp, production_line_id)

        start_time = timestamp - timedelta(minutes=time_range_minutes)
        end_time = timestamp + timedelta(minutes=time_range_minutes)

        images = self.image_storage.get_images(
            start_time=start_time,
            end_time=end_time,
            production_line_id=production_line_id,
        )

        return images

    def _handle_get_images(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle get_images request from another agent.

        Args:
            payload: Request payload containing timestamp, time_range, etc.

        Returns:
            Response with image analysis
        """
        timestamp_str = payload.get("timestamp")
        timestamp = datetime.fromisoformat(timestamp_str)
        time_range = payload.get("time_range_minutes", 5)
        reason = payload.get("reason", "Investigation")
        context = payload.get("context", {})

        # Retrieve images
        images = self.process(
            timestamp=timestamp,
            time_range_minutes=time_range,
            production_line_id=context.get("production_line_id"),
        )

        if not images:
            return {
                "status": "no_images_found",
                "timestamp": timestamp_str,
                "analysis": "No images found for the specified time range.",
            }

        # Analyze images with LLM
        analysis = self._analyze_images(images, reason, context)

        return {
            "status": "success",
            "timestamp": timestamp_str,
            "images_found": len(images),
            "image_metadata": [img.to_dict() for img in images],
            "analysis": analysis,
        }

    def _analyze_images(
        self,
        images: List[ImageMetadata],
        reason: str,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Analyze images using LLM.

        Args:
            images: List of image metadata
            reason: Reason for requesting images
            context: Additional context from time series analysis

        Returns:
            Analysis results
        """
        if self.llm_client is None:
            return {
                "summary": "Mock image analysis - LLM client not configured",
                "observations": [],
            }

        # Prepare prompt for image analysis
        prompt = self._prepare_image_analysis_prompt(images, reason, context)

        try:
            response = self.llm_client.generate(prompt)
            if isinstance(response, str):
                import re
                json_match = re.search(r"\{.*\}", response, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
                return json.loads(response)
            return response
        except Exception as e:
            return {
                "summary": f"Image analysis error: {str(e)}",
                "observations": [],
            }

    def _prepare_image_analysis_prompt(
        self,
        images: List[ImageMetadata],
        reason: str,
        context: Dict[str, Any],
    ) -> str:
        """Prepare prompt for LLM image analysis."""
        image_info = []
        for img in images:
            image_info.append({
                "timestamp": img.timestamp.isoformat(),
                "production_line_id": img.production_line_id,
                "image_path": img.image_path,
                "quality_flags": img.quality_flags,
                "associated_statistics": (
                    img.associated_statistics.to_dict()
                    if img.associated_statistics
                    else None
                ),
            })

        prompt = f"""You are analyzing production line images to investigate a quality issue.

Reason for Investigation: {reason}

Context from Time Series Analysis:
{json.dumps(context, indent=2)}

Available Images:
{json.dumps(image_info, indent=2)}

Please analyze these images and provide:
1. Visual observations (defects, anomalies, quality issues)
2. Correlation with the time series data context
3. Root cause hypotheses
4. Confidence level in your observations

Note: The actual image files are available at the paths specified above. 
In a real implementation, you would process the image pixels directly.

Respond in JSON format:
{{
    "summary": "Overall visual assessment",
    "observations": [
        {{
            "image_timestamp": "...",
            "finding": "...",
            "severity": "low|medium|high",
            "confidence": 0.0-1.0
        }}
    ],
    "root_cause_hypotheses": ["hypothesis 1", ...],
    "recommendations": ["recommendation 1", ...]
}}
"""

        return prompt

    def _get_mock_images(
        self, timestamp: datetime, production_line_id: Optional[str]
    ) -> List[ImageMetadata]:
        """Generate mock images for testing."""
        return [
            ImageMetadata(
                timestamp=timestamp,
                production_line_id=production_line_id or "line_1",
                image_path=f"/images/line_1/{timestamp.isoformat()}.jpg",
                quality_flags=["defect_detected"],
            )
        ]
