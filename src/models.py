"""
Data models for production quality analysis system.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum


class DefectType(str, Enum):
    """Types of defects that can be detected."""
    SCRATCH = "scratch"
    DISCOLORATION = "discoloration"
    MISSING_PART = "missing_part"
    SIZE_VARIATION = "size_variation"
    SHAPE_DEFORMITY = "shape_deformity"
    SURFACE_DEFECT = "surface_defect"
    OTHER = "other"


@dataclass
class ProductionStatistics:
    """Daily production statistics for a production line."""
    date: datetime
    production_line_id: str
    object_count: int
    average_size: float
    defect_count: int
    defect_types: Dict[DefectType, int]
    color_distribution: Dict[str, int]  # color_name -> count
    throughput_per_hour: float
    shift: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "date": self.date.isoformat(),
            "production_line_id": self.production_line_id,
            "object_count": self.object_count,
            "average_size": self.average_size,
            "defect_count": self.defect_count,
            "defect_types": {k.value: v for k, v in self.defect_types.items()},
            "color_distribution": self.color_distribution,
            "throughput_per_hour": self.throughput_per_hour,
            "shift": self.shift,
            "metadata": self.metadata or {},
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProductionStatistics":
        """Create from dictionary."""
        return cls(
            date=datetime.fromisoformat(data["date"]),
            production_line_id=data["production_line_id"],
            object_count=data["object_count"],
            average_size=data["average_size"],
            defect_count=data["defect_count"],
            defect_types={
                DefectType(k): v for k, v in data["defect_types"].items()
            },
            color_distribution=data["color_distribution"],
            throughput_per_hour=data["throughput_per_hour"],
            shift=data.get("shift"),
            metadata=data.get("metadata"),
        )


@dataclass
class ImageMetadata:
    """Metadata for production line images."""
    timestamp: datetime
    production_line_id: str
    image_path: str
    image_url: Optional[str] = None
    associated_statistics: Optional[ProductionStatistics] = None
    quality_flags: List[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if self.quality_flags is None:
            self.quality_flags = []

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "production_line_id": self.production_line_id,
            "image_path": self.image_path,
            "image_url": self.image_url,
            "associated_statistics": (
                self.associated_statistics.to_dict()
                if self.associated_statistics
                else None
            ),
            "quality_flags": self.quality_flags,
            "metadata": self.metadata or {},
        }


@dataclass
class AgentMessage:
    """Message structure for inter-agent communication."""
    from_agent: str
    to_agent: str
    request_type: str
    payload: Dict[str, Any]
    timestamp: datetime
    correlation_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "from_agent": self.from_agent,
            "to_agent": self.to_agent,
            "request_type": self.request_type,
            "payload": self.payload,
            "timestamp": self.timestamp.isoformat(),
            "correlation_id": self.correlation_id,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentMessage":
        """Create from dictionary."""
        return cls(
            from_agent=data["from_agent"],
            to_agent=data["to_agent"],
            request_type=data["request_type"],
            payload=data["payload"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            correlation_id=data.get("correlation_id"),
        )


@dataclass
class QualityInsight:
    """Generated insight about production quality."""
    insight_type: str  # "anomaly", "trend", "recommendation", "alert"
    severity: str  # "low", "medium", "high", "critical"
    title: str
    description: str
    timestamp: datetime
    production_line_id: str
    supporting_data: Dict[str, Any]
    recommended_actions: List[str]
    confidence: float  # 0.0 to 1.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "insight_type": self.insight_type,
            "severity": self.severity,
            "title": self.title,
            "description": self.description,
            "timestamp": self.timestamp.isoformat(),
            "production_line_id": self.production_line_id,
            "supporting_data": self.supporting_data,
            "recommended_actions": self.recommended_actions,
            "confidence": self.confidence,
        }
