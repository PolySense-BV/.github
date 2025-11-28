"""
Example using real LLM clients (OpenAI or Gemini).
"""

from datetime import datetime, timedelta
import os
from src.agent_orchestrator import AgentOrchestrator
from src.models import ProductionStatistics, DefectType
from src.llm_client import OpenAILLMClient, GeminiLLMClient
from src.storage import MockImageStorage


def create_sample_data() -> list[ProductionStatistics]:
    """Create sample production statistics."""
    stats = []
    base_date = datetime(2024, 1, 1)

    for day in range(7):
        date = base_date + timedelta(days=day)
        stats.append(
            ProductionStatistics(
                date=date,
                production_line_id="line_1",
                object_count=1000 + (day * 50),
                average_size=10.5 + (day * 0.1),
                defect_count=5 + (day * 2),
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
    """Run example with real LLM."""
    print("Multi-Agent System with Real LLM")
    print("=" * 70)

    # Choose LLM provider
    llm_provider = os.getenv("LLM_PROVIDER", "openai")  # or "gemini"
    api_key = os.getenv("LLM_API_KEY")

    if not api_key:
        print("ERROR: LLM_API_KEY environment variable not set")
        print("Set it with: export LLM_API_KEY=your_key_here")
        return

    # Initialize LLM client
    if llm_provider == "openai":
        llm_client = OpenAILLMClient(api_key=api_key, model="gpt-4")
        print("Using OpenAI GPT-4")
    elif llm_provider == "gemini":
        llm_client = GeminiLLMClient(api_key=api_key, model="gemini-pro")
        print("Using Google Gemini Pro")
    else:
        print(f"Unknown LLM provider: {llm_provider}")
        return

    # Initialize storage
    image_storage = MockImageStorage()

    # Create orchestrator
    orchestrator = AgentOrchestrator(
        llm_client=llm_client,
        image_storage=image_storage,
    )

    print(f"Initialized agents: {orchestrator.list_agents()}")
    print()

    # Load data
    print("Loading production data...")
    time_series_data = create_sample_data()
    print(f"Loaded {len(time_series_data)} days of production statistics")
    print()

    # Analyze
    print("Analyzing production quality (this may take a moment)...")
    print("-" * 70)
    insights = orchestrator.analyze_production_quality(
        time_series_data=time_series_data,
        time_period="Past 7 days",
    )

    # Display results
    print(f"\nGenerated {len(insights)} insights:\n")
    for i, insight in enumerate(insights, 1):
        print(f"Insight {i}:")
        print(f"  Type: {insight.insight_type}")
        print(f"  Severity: {insight.severity}")
        print(f"  Title: {insight.title}")
        print(f"  Description: {insight.description}")
        print(f"  Confidence: {insight.confidence:.2f}")
        if insight.recommended_actions:
            print(f"  Recommended Actions:")
            for action in insight.recommended_actions:
                print(f"    - {action}")
        print()

    print("=" * 70)
    print("Analysis complete!")


if __name__ == "__main__":
    main()
