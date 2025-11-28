"""
Example usage of the multi-agent production quality analysis system.
"""

from datetime import datetime, timedelta
from src.agent_orchestrator import AgentOrchestrator
from src.models import ProductionStatistics, DefectType
from src.llm_client import MockLLMClient
from src.storage import MockImageStorage


def create_sample_data() -> list[ProductionStatistics]:
    """Create sample production statistics for demonstration."""
    stats = []
    base_date = datetime(2024, 1, 1)

    for day in range(7):  # 7 days of data
        date = base_date + timedelta(days=day)
        stats.append(
            ProductionStatistics(
                date=date,
                production_line_id="line_1",
                object_count=1000 + (day * 50),
                average_size=10.5 + (day * 0.1),
                defect_count=5 + (day * 2),  # Increasing defects
                defect_types={
                    DefectType.SCRATCH: 2 + day,
                    DefectType.DISCOLORATION: 1,
                    DefectType.SIZE_VARIATION: 2 + day,
                },
                color_distribution={
                    "red": 300 + (day * 20),
                    "blue": 400 + (day * 15),
                    "green": 300 + (day * 15),
                },
                throughput_per_hour=100.0 + (day * 2),
                shift="day",
            )
        )

    return stats


def main():
    """Run example analysis."""
    print("Initializing Multi-Agent Production Quality Analysis System...")
    print("=" * 70)

    # Initialize components
    llm_client = MockLLMClient()
    image_storage = MockImageStorage()

    # Create orchestrator
    orchestrator = AgentOrchestrator(
        llm_client=llm_client,
        image_storage=image_storage,
    )

    print(f"Initialized agents: {orchestrator.list_agents()}")
    print()

    # Create sample data
    print("Loading production data...")
    time_series_data = create_sample_data()
    print(f"Loaded {len(time_series_data)} days of production statistics")
    print()

    # Analyze production quality
    print("Analyzing production quality...")
    print("-" * 70)
    insights = orchestrator.analyze_production_quality(
        time_series_data=time_series_data,
        time_period="Past 7 days",
    )

    # Display insights
    print(f"\nGenerated {len(insights)} insights:\n")
    for i, insight in enumerate(insights, 1):
        print(f"Insight {i}:")
        print(f"  Type: {insight.insight_type}")
        print(f"  Severity: {insight.severity}")
        print(f"  Title: {insight.title}")
        print(f"  Description: {insight.description}")
        print(f"  Confidence: {insight.confidence:.2f}")
        print(f"  Recommended Actions:")
        for action in insight.recommended_actions:
            print(f"    - {action}")
        print()

    print("=" * 70)
    print("Analysis complete!")


if __name__ == "__main__":
    main()
