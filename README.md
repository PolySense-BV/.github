# Multi-Agent Production Quality Analysis System

A sophisticated multi-agent system that analyzes production quality data using LLM-powered reasoning. The system processes time series production statistics and can intelligently request and analyze production line images when deeper investigation is needed.

## Overview

This system is designed to assist production line managers by providing intelligent insights about production quality. Instead of replacing quality operators, it replaces the need for constant manual monitoring by line operators and managers, offering:

- **Automated Quality Analysis**: Daily analysis of production statistics
- **Intelligent Image Retrieval**: Images are fetched only when the LLM determines they're needed
- **Actionable Insights**: Clear recommendations based on data and visual evidence
- **Multi-Agent Architecture**: Specialized agents for different tasks

## Architecture

The system consists of two main agents:

1. **Time Series Analysis Agent** (Orchestrator)
   - Analyzes daily production statistics
   - Identifies trends, anomalies, and patterns
   - Coordinates with other agents
   - Generates comprehensive insights

2. **Image Retrieval Agent**
   - Fetches production line images on demand
   - Analyzes images when requested by the orchestrator
   - Provides visual context for quality issues

### Data Flow

```
Production Data → Time Series Agent → LLM Analysis
                                      ↓
                              Need Images?
                                      ↓ Yes
                              Image Retrieval Agent
                                      ↓
                              Image Analysis
                                      ↓
                              Combined Insights
                                      ↓
                              Production Manager
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Install LLM client packages:
```bash
# For OpenAI
pip install openai

# For Google Gemini
pip install google-generativeai
```

## Usage

### Basic Example (Mock LLM)

```python
from src.agent_orchestrator import AgentOrchestrator
from src.llm_client import MockLLMClient
from src.storage import MockImageStorage
from src.models import ProductionStatistics

# Initialize
orchestrator = AgentOrchestrator(
    llm_client=MockLLMClient(),
    image_storage=MockImageStorage(),
)

# Load your production data
time_series_data = [...]  # List of ProductionStatistics

# Analyze
insights = orchestrator.analyze_production_quality(
    time_series_data=time_series_data,
    time_period="Past 7 days",
)

# Use insights
for insight in insights:
    print(f"{insight.severity}: {insight.title}")
    print(insight.description)
    print(f"Actions: {insight.recommended_actions}")
```

### With Real LLM

Set environment variables:
```bash
export LLM_PROVIDER=openai  # or "gemini"
export LLM_API_KEY=your_api_key_here
```

Then run:
```bash
python examples/with_real_llm.py
```

## Data Models

### ProductionStatistics

Daily production statistics including:
- Object count, size, defects
- Defect types and distribution
- Color distribution
- Throughput metrics
- Production line and shift information

### ImageMetadata

Image information including:
- Timestamp and production line ID
- Image path/URL
- Associated statistics snapshot
- Quality flags

### QualityInsight

Generated insights with:
- Type (anomaly, trend, recommendation, alert)
- Severity (low, medium, high, critical)
- Description and recommendations
- Confidence score
- Supporting data

## Agent Communication

Agents communicate via structured JSON messages:

```json
{
  "from_agent": "time_series_agent",
  "to_agent": "image_retrieval_agent",
  "request_type": "get_images",
  "payload": {
    "timestamp": "2024-01-15T14:30:00",
    "time_range_minutes": 5,
    "reason": "Anomaly detected in defect rate"
  }
}
```

## Extending the System

### Adding New Agents

1. Create a new agent class inheriting from `BaseAgent`:
```python
from src.agents.base_agent import BaseAgent

class MyNewAgent(BaseAgent):
    def process(self, input_data):
        # Your processing logic
        pass
```

2. Register it in the orchestrator:
```python
orchestrator.agents["my_agent"] = MyNewAgent()
```

### Custom LLM Clients

Implement the `BaseLLMClient` interface:
```python
from src.llm_client import BaseLLMClient

class MyLLMClient(BaseLLMClient):
    def generate(self, prompt: str, **kwargs) -> str:
        # Your LLM integration
        return response
```

### Custom Image Storage

Implement the `BaseImageStorage` interface:
```python
from src.storage import BaseImageStorage

class MyImageStorage(BaseImageStorage):
    def get_images(self, start_time, end_time, production_line_id=None):
        # Your storage logic
        return images
```

## Examples

See the `examples/` directory for:
- `basic_usage.py`: Simple example with mock LLM
- `with_real_llm.py`: Example using real LLM APIs

## Configuration

The system is designed to be flexible. Key configuration points:

- **LLM Provider**: Choose OpenAI, Gemini, or implement your own
- **Image Storage**: File system, database, cloud storage, etc.
- **Analysis Frequency**: Daily, hourly, or on-demand
- **Time Ranges**: Configurable for different analysis periods

## Design Principles

1. **Agent Autonomy**: Each agent has a specific role
2. **Request-Response Pattern**: Clean communication protocol
3. **LLM-Powered Reasoning**: Intelligent decision-making
4. **Contextual Retrieval**: Images fetched only when needed
5. **Extensibility**: Easy to add new agents or capabilities

## Use Cases

- **Daily Quality Review**: Automated analysis of daily production
- **Anomaly Detection**: Early warning of quality issues
- **Trend Analysis**: Long-term quality patterns
- **Root Cause Analysis**: Deep investigation with visual evidence
- **Predictive Insights**: Forecasting potential issues

## Contributing

1. Follow the code style (black, flake8)
2. Add type hints to all functions
3. Include docstrings
4. Write tests for new features
5. Update documentation

## License

[Your License Here]

## Support

For questions or issues, please open an issue in the repository.
