# Multi-Agent Production Quality Analysis System

## Overview

This system uses a multi-agent architecture to analyze production quality data over time, providing insights that help production line managers make informed decisions. The system processes time series data (statistics, counts, defects) and can request specific images for deeper analysis when anomalies or patterns are detected.

## System Architecture

### Core Agents

1. **Time Series Analysis Agent (Orchestrator)**
   - Primary agent that receives daily production data
   - Analyzes time series patterns using LLM reasoning
   - Identifies noteworthy trends, anomalies, and patterns
   - Coordinates with other agents to gather additional context
   - Generates actionable insights for production managers

2. **Image Retrieval Agent**
   - Specialized agent for fetching and analyzing production line images
   - Responds to requests from the Time Series Analysis Agent
   - Can retrieve images by timestamp, time range, or specific criteria
   - Provides image analysis summaries back to the orchestrator

### Data Flow

```
Production Data Sources
    ↓
Time Series Analysis Agent (Daily Batch)
    ↓
LLM Analysis (Pattern Detection)
    ↓
Decision Point: Need Images?
    ├─ No → Generate Insights
    └─ Yes → Request Image Retrieval Agent
              ↓
         Image Retrieval Agent
              ↓
         Fetch & Analyze Images
              ↓
         Return Image Insights
              ↓
    Time Series Analysis Agent
              ↓
    Generate Comprehensive Insights
              ↓
    Production Manager Dashboard/Reports
```

## Key Design Principles

1. **Agent Autonomy**: Each agent has a specific role and can operate independently
2. **Request-Response Pattern**: Agents communicate via structured messages
3. **LLM-Powered Reasoning**: Both agents use LLMs for intelligent analysis
4. **Contextual Image Retrieval**: Images are fetched only when needed for deeper analysis
5. **Time-Aware Analysis**: System understands temporal patterns and trends

## Data Models

### Production Statistics (Daily)
- Date/Time
- Object count
- Average size
- Defect count and types
- Color distribution
- Production line ID
- Shift information
- Throughput metrics

### Image Metadata
- Timestamp
- Production line ID
- Image path/URL
- Associated statistics snapshot
- Quality flags

## Agent Communication Protocol

Agents communicate via structured JSON messages:

```json
{
  "from": "time_series_agent",
  "to": "image_retrieval_agent",
  "request_type": "get_images",
  "timestamp": "2024-01-15T14:30:00",
  "time_range": "±5 minutes",
  "reason": "Anomaly detected in defect rate",
  "context": {...}
}
```

## Use Cases

1. **Daily Quality Review**: Analyze past 24 hours of production data
2. **Anomaly Detection**: Identify unusual patterns and investigate with images
3. **Trend Analysis**: Long-term quality trends over weeks/months
4. **Root Cause Analysis**: Deep dive into specific quality issues
5. **Predictive Insights**: Forecast potential quality issues

## Benefits

- **Proactive Management**: Early detection of quality issues
- **Data-Driven Decisions**: Evidence-based insights for line operators/managers
- **Efficient Resource Use**: Images retrieved only when needed
- **Scalable**: Can handle multiple production lines
- **Explainable**: LLM provides reasoning for insights
