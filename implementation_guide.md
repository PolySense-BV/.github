# Multi-Agent Production Quality System - Implementation Guide

This guide provides practical steps to implement the multi-agent production quality analysis system in a real manufacturing environment.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Architecture Decisions](#architecture-decisions)
3. [Phase-by-Phase Implementation](#phase-by-phase-implementation)
4. [Technology Stack](#technology-stack)
5. [Integration Points](#integration-points)
6. [Deployment Guide](#deployment-guide)
7. [Cost Analysis](#cost-analysis)
8. [Monitoring & Maintenance](#monitoring--maintenance)

---

## Prerequisites

### Data Requirements

#### 1. Time-Series Production Data
Your system must already collect:
- **Metrics** (per minute/hour):
  - Production counts (units per time period)
  - Defect counts (by type)
  - Process parameters (temperature, pressure, speed, etc.)
  - Machine telemetry (cycle times, downtime, etc.)
  
- **Format**: Any time-series format (InfluxDB, TimescaleDB, CSV, JSON)
- **Retention**: At least 90 days for pattern analysis
- **Granularity**: Ideally 1-minute intervals, minimum 1-hour aggregations

#### 2. Production Line Images
Your system must capture:
- **Images**: Regular captures from line cameras
- **Frequency**: Every 1-5 minutes minimum
- **Storage**: Cloud storage (S3, Azure Blob, etc.) or NAS
- **Metadata**: Timestamp, line ID, camera ID
- **Quality**: Sufficient resolution for defect detection (1920x1080 minimum)
- **Retention**: At least 30 days

#### 3. Historical Records
- Defect/incident logs
- Maintenance records
- Root cause analysis documents
- Equipment specifications

### Infrastructure Requirements

- **Cloud Platform**: AWS, Azure, or GCP (or hybrid)
- **Compute**: 
  - Development: 4 CPU, 16GB RAM minimum
  - Production: 8-16 CPU, 32-64GB RAM (for concurrent analysis)
- **Storage**:
  - Time-series database: 100GB+ depending on volume
  - Image storage: 500GB - 5TB depending on retention
  - Vector database: 10-50GB
- **Network**: Stable connection between factory floor and cloud (if hybrid)

### Team Requirements

- **Data Engineer** (1): Set up data pipelines, databases
- **ML Engineer** (1): Implement agents, integrate LLM APIs
- **DevOps Engineer** (0.5): Deploy infrastructure, monitoring
- **Domain Expert** (0.5): Quality engineer to validate system
- **Project Manager** (0.5): Coordinate implementation

**Timeline**: 6-8 weeks for MVP, 12-16 weeks for full deployment

---

## Architecture Decisions

### Decision 1: Cloud vs. On-Premise

| Aspect | Cloud | On-Premise | Hybrid (Recommended) |
|--------|-------|------------|----------------------|
| **LLM API** | ✅ Cloud APIs (Claude, GPT) | ❌ Not feasible | ✅ Cloud APIs |
| **Data Storage** | ✅ Cloud storage | ✅ Factory servers | ✅ Local + cloud sync |
| **Image Processing** | ✅ Cloud compute | ⚠️ Requires GPU servers | ✅ Edge + cloud |
| **Latency** | ⚠️ Network dependent | ✅ Low latency | ✅ Optimized |
| **Cost** | ⚠️ Ongoing API costs | ⚠️ High upfront | ✅ Balanced |
| **Security** | ⚠️ Data leaves premises | ✅ Data stays internal | ✅ Configurable |

**Recommended: Hybrid Architecture**
- **Factory Floor**: Local data collection, time-series DB
- **Edge/Gateway**: Pre-processing, data aggregation
- **Cloud**: LLM agents, long-term storage, analytics

### Decision 2: LLM Provider Selection

| Provider | Model | Pros | Cons | Cost (per analysis) |
|----------|-------|------|------|---------------------|
| **Anthropic** | Claude 3.5 Sonnet | Best reasoning, vision, long context | No fine-tuning yet | $0.20-0.30 |
| **OpenAI** | GPT-4 Turbo | Good ecosystem, fine-tuning | Higher cost, rate limits | $0.25-0.40 |
| **OpenAI** | GPT-4o | Vision, fast | Less sophisticated reasoning | $0.15-0.25 |
| **Google** | Gemini 1.5 Pro | Good vision, free tier | Less consistent | $0.10-0.20 |
| **Open Source** | Llama 3 70B | No API costs, privacy | Self-hosting complexity | $0.05-0.10 (compute) |

**Recommended: Anthropic Claude 3.5 Sonnet**
- Best reasoning capabilities for root cause analysis
- Excellent vision for image analysis
- Long context window (200k tokens) for historical data
- Reliable structured output

**Alternative: Hybrid Approach**
- Claude for complex reasoning & synthesis
- GPT-4o for image analysis (faster, cheaper)
- Open-source for simple queries/classification

### Decision 3: Agent Framework

| Framework | Description | Best For |
|-----------|-------------|----------|
| **LangGraph** | Agent workflow orchestration | Complex multi-agent workflows |
| **CrewAI** | Purpose-built multi-agent | Rapid prototyping |
| **AutoGen** | Microsoft's multi-agent | Research-heavy projects |
| **Custom** | Build from scratch | Full control, specific needs |

**Recommended: LangGraph**
- Mature, production-ready
- Excellent for state management
- Good debugging tools
- Strong community support

**Alternative: Custom Implementation** (for full control)
- Use our example code as starting point
- Direct API calls to Claude/GPT
- Custom orchestration logic

---

## Phase-by-Phase Implementation

### Phase 1: Data Infrastructure (Weeks 1-2)

**Goal**: Set up data pipelines and storage

#### Step 1.1: Time-Series Database Setup

```bash
# Option A: TimescaleDB (PostgreSQL extension)
docker run -d --name timescaledb \
  -p 5432:5432 \
  -e POSTGRES_PASSWORD=password \
  timescale/timescaledb:latest-pg14

# Create production metrics table
psql -h localhost -U postgres -d postgres <<EOF
CREATE TABLE production_metrics (
  time TIMESTAMPTZ NOT NULL,
  line_id TEXT NOT NULL,
  metric_name TEXT NOT NULL,
  metric_value DOUBLE PRECISION NOT NULL,
  metadata JSONB
);

SELECT create_hypertable('production_metrics', 'time');

CREATE INDEX idx_line_time ON production_metrics (line_id, time DESC);
CREATE INDEX idx_metric ON production_metrics (metric_name, time DESC);
EOF
```

```python
# Data ingestion script
from datetime import datetime
import psycopg2

def ingest_production_data(line_id, metrics):
    """Ingest production metrics into TimescaleDB"""
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="password"
    )
    
    with conn.cursor() as cur:
        for metric_name, value in metrics.items():
            cur.execute(
                """
                INSERT INTO production_metrics (time, line_id, metric_name, metric_value)
                VALUES (%s, %s, %s, %s)
                """,
                (datetime.now(), line_id, metric_name, value)
            )
    
    conn.commit()
    conn.close()

# Example usage
ingest_production_data("Line_3", {
    "defect_rate": 0.0085,
    "temperature": 85.2,
    "cycle_time": 1250,
    "total_units": 5140
})
```

#### Step 1.2: Image Storage Setup

```python
# Image storage with metadata
import boto3
from datetime import datetime
import json

class ProductionImageStore:
    def __init__(self):
        self.s3 = boto3.client('s3')
        self.bucket = 'production-images'
    
    def store_image(self, image_data, line_id, camera_id, metadata=None):
        """Store production image with metadata"""
        timestamp = datetime.now()
        
        # Generate key: YYYY/MM/DD/HH/line_camera_timestamp.jpg
        key = timestamp.strftime(
            f"%Y/%m/%d/%H/{line_id}_{camera_id}_%Y%m%d_%H%M%S.jpg"
        )
        
        # Metadata
        image_metadata = {
            "line_id": line_id,
            "camera_id": camera_id,
            "timestamp": timestamp.isoformat(),
            **(metadata or {})
        }
        
        # Upload to S3
        self.s3.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=image_data,
            Metadata={k: str(v) for k, v in image_metadata.items()}
        )
        
        return key
    
    def retrieve_images(self, line_id, start_time, end_time):
        """Retrieve images in time range"""
        # Generate prefix from start time
        prefix = start_time.strftime(f"%Y/%m/%d/%H/{line_id}")
        
        response = self.s3.list_objects_v2(
            Bucket=self.bucket,
            Prefix=prefix
        )
        
        images = []
        for obj in response.get('Contents', []):
            # Filter by time range
            # ... (implement time filtering)
            images.append(obj['Key'])
        
        return images
```

#### Step 1.3: Vector Database for Knowledge Base

```python
# Using Pinecone for historical incident search
import pinecone
from openai import OpenAI

# Initialize
pinecone.init(api_key="your-api-key", environment="us-west1-gcp")
index = pinecone.Index("production-incidents")

openai_client = OpenAI(api_key="your-api-key")

def store_incident(incident_data):
    """Store incident with embedding for similarity search"""
    # Create text description
    text = f"""
    Line: {incident_data['line_id']}
    Date: {incident_data['date']}
    Symptoms: {incident_data['symptoms']}
    Root Cause: {incident_data['root_cause']}
    Resolution: {incident_data['resolution']}
    """
    
    # Generate embedding
    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    embedding = response.data[0].embedding
    
    # Store in Pinecone
    index.upsert([(
        incident_data['incident_id'],
        embedding,
        incident_data
    )])

def search_similar_incidents(query_text, top_k=5):
    """Search for similar historical incidents"""
    # Generate query embedding
    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=query_text
    )
    query_embedding = response.data[0].embedding
    
    # Search
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )
    
    return [match['metadata'] for match in results['matches']]
```

### Phase 2: Core Agent Implementation (Weeks 3-4)

**Goal**: Implement the three core agents (Orchestrator, Time Series, Image)

#### Step 2.1: Set Up LLM API Access

```python
# config.py
from dataclasses import dataclass

@dataclass
class LLMConfig:
    # Anthropic Claude for reasoning
    anthropic_api_key: str
    anthropic_model: str = "claude-3-5-sonnet-20241022"
    
    # Optional: OpenAI for embeddings
    openai_api_key: str = None
    
    # Cost tracking
    track_costs: bool = True
    
    # Rate limiting
    max_requests_per_minute: int = 50

# Initialize
from anthropic import Anthropic

config = LLMConfig(
    anthropic_api_key="your-api-key-here"
)

anthropic_client = Anthropic(api_key=config.anthropic_api_key)
```

#### Step 2.2: Implement Time Series Agent

```python
# agents/time_series_agent.py
from anthropic import Anthropic
import json
from typing import List, Dict
import statistics

class TimeSeriesAnalysisAgent:
    def __init__(self, anthropic_client: Anthropic):
        self.client = anthropic_client
        self.system_prompt = """You are an expert in statistical process control and time series analysis.
        
        Your role is to analyze production statistics and identify:
        1. Statistical anomalies and outliers
        2. Trends (degradation or improvement)
        3. Correlations between variables
        4. Time periods requiring deeper investigation
        
        When you identify patterns, you should:
        - Quantify the deviation from normal
        - Assess the business impact
        - Recommend whether visual inspection is needed
        - Suggest specific time ranges for image analysis
        
        You have access to statistical tools. Call them when needed.
        
        Always provide:
        - Confidence scores (0-1)
        - Quantified impacts
        - Structured recommendations
        """
        
        self.tools = [
            {
                "name": "calculate_statistics",
                "description": "Calculate mean, std dev, min, max for a data series",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "values": {
                            "type": "array",
                            "items": {"type": "number"},
                            "description": "Array of numeric values"
                        }
                    },
                    "required": ["values"]
                }
            },
            {
                "name": "detect_anomalies",
                "description": "Detect outliers using Z-score method",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "values": {
                            "type": "array",
                            "items": {"type": "number"}
                        },
                        "threshold": {
                            "type": "number",
                            "description": "Z-score threshold (default 3.0)"
                        }
                    },
                    "required": ["values"]
                }
            },
            {
                "name": "correlation_analysis",
                "description": "Calculate correlation coefficient between two variables",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "x": {"type": "array", "items": {"type": "number"}},
                        "y": {"type": "array", "items": {"type": "number"}}
                    },
                    "required": ["x", "y"]
                }
            }
        ]
    
    async def analyze(self, production_data: List[Dict]) -> Dict:
        """
        Analyze time-series production data
        """
        # Format data for LLM
        data_json = json.dumps(production_data, indent=2)
        
        # Initial analysis request
        messages = [{
            "role": "user",
            "content": f"""Analyze the following production data and identify any quality issues, patterns, or anomalies.

Production Data:
{data_json}

For each finding:
1. Describe the pattern/anomaly
2. Quantify the deviation (use statistical tools)
3. Assess business impact
4. Recommend if visual inspection is needed

Return your analysis in structured JSON format with this schema:
{{
  "findings": [
    {{
      "type": "anomaly|trend|correlation",
      "description": "Clear description",
      "severity": "low|medium|high",
      "metrics": {{}},
      "confidence": 0.0-1.0
    }}
  ],
  "statistics": {{}},
  "requires_images": boolean,
  "image_requests": [
    {{
      "time_range": ["start", "end"],
      "line_id": "string",
      "reason": "string"
    }}
  ]
}}"""
        }]
        
        # Agentic loop - let Claude use tools
        while True:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4096,
                system=self.system_prompt,
                tools=self.tools,
                messages=messages
            )
            
            # Check if Claude wants to use tools
            if response.stop_reason == "tool_use":
                # Execute tool calls
                tool_results = []
                for content in response.content:
                    if content.type == "tool_use":
                        result = self._execute_tool(content.name, content.input)
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": content.id,
                            "content": json.dumps(result)
                        })
                
                # Add Claude's response and tool results to conversation
                messages.append({"role": "assistant", "content": response.content})
                messages.append({"role": "user", "content": tool_results})
                
                # Continue loop - Claude will process tool results
                continue
            
            else:
                # Claude is done, extract final answer
                for content in response.content:
                    if content.type == "text":
                        # Parse JSON from text
                        analysis_result = self._parse_json(content.text)
                        return analysis_result
                
                break
        
        return {}
    
    def _execute_tool(self, tool_name: str, tool_input: Dict):
        """Execute statistical tools"""
        if tool_name == "calculate_statistics":
            values = tool_input["values"]
            return {
                "mean": statistics.mean(values),
                "stdev": statistics.stdev(values) if len(values) > 1 else 0,
                "min": min(values),
                "max": max(values)
            }
        
        elif tool_name == "detect_anomalies":
            values = tool_input["values"]
            threshold = tool_input.get("threshold", 3.0)
            mean = statistics.mean(values)
            stdev = statistics.stdev(values) if len(values) > 1 else 0
            
            anomalies = []
            for i, value in enumerate(values):
                if stdev > 0:
                    z_score = abs((value - mean) / stdev)
                    if z_score > threshold:
                        anomalies.append({
                            "index": i,
                            "value": value,
                            "z_score": z_score
                        })
            
            return {"anomalies": anomalies}
        
        elif tool_name == "correlation_analysis":
            x = tool_input["x"]
            y = tool_input["y"]
            
            if len(x) != len(y) or len(x) < 2:
                return {"correlation": 0.0, "error": "Invalid data"}
            
            mean_x = statistics.mean(x)
            mean_y = statistics.mean(y)
            
            numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x)))
            denom_x = sum((x[i] - mean_x) ** 2 for i in range(len(x)))
            denom_y = sum((y[i] - mean_y) ** 2 for i in range(len(y)))
            
            if denom_x == 0 or denom_y == 0:
                return {"correlation": 0.0}
            
            correlation = numerator / (denom_x * denom_y) ** 0.5
            return {"correlation": correlation}
        
        return {}
    
    def _parse_json(self, text: str) -> Dict:
        """Extract and parse JSON from text"""
        # Try to find JSON in text
        import re
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except:
                pass
        return {}
```

#### Step 2.3: Implement Image Analysis Agent

```python
# agents/image_analysis_agent.py
from anthropic import Anthropic
import base64
from typing import List, Dict

class ImageAnalysisAgent:
    def __init__(self, anthropic_client: Anthropic, image_store):
        self.client = anthropic_client
        self.image_store = image_store
        self.system_prompt = """You are a visual quality inspection expert.
        
        Analyze production line images and identify:
        - Visual defects and their types
        - Defect severity and patterns
        - Changes over time
        - Visual evidence supporting/refuting hypotheses
        
        Describe what you see clearly and relate it to production quality.
        """
    
    async def analyze(self, request: Dict) -> Dict:
        """
        Analyze images based on request
        """
        # Retrieve images
        images = self.image_store.retrieve_images(
            line_id=request["line_id"],
            start_time=request["time_range"][0],
            end_time=request["time_range"][1]
        )
        
        # Sample images (don't send all to avoid cost)
        sampled_images = self._sample_images(images, max_images=12)
        
        # Prepare image content for Claude
        image_content = []
        for img_key in sampled_images:
            # Download image
            img_data = self.image_store.download_image(img_key)
            
            # Encode as base64
            img_base64 = base64.b64encode(img_data).decode('utf-8')
            
            image_content.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": img_base64
                }
            })
        
        # Create prompt
        context = request.get("context", {})
        prompt = f"""Analyze these {len(sampled_images)} production line images.

Context: {context.get('hypothesis', 'General quality inspection')}

Statistical Evidence:
{json.dumps(context.get('statistical_evidence', {}), indent=2)}

For each image:
1. Identify any defects or quality issues
2. Classify defect type and severity
3. Look for patterns across the time period

Return structured JSON analysis."""

        # Call Claude with vision
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            system=self.system_prompt,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    *image_content
                ]
            }]
        )
        
        # Parse response
        analysis = self._parse_response(response.content[0].text)
        return analysis
    
    def _sample_images(self, images: List[str], max_images: int = 12) -> List[str]:
        """Sample images evenly across time period"""
        if len(images) <= max_images:
            return images
        
        # Sample evenly
        step = len(images) / max_images
        return [images[int(i * step)] for i in range(max_images)]
    
    def _parse_response(self, text: str) -> Dict:
        """Parse visual analysis response"""
        # Similar to time series agent
        import json
        import re
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except:
                pass
        return {"visual_findings": [], "patterns": []}
```

#### Step 2.4: Implement Orchestrator

```python
# agents/orchestrator.py
from anthropic import Anthropic
from typing import Dict, List

class OrchestratorAgent:
    def __init__(
        self,
        anthropic_client: Anthropic,
        time_series_agent,
        image_agent,
        knowledge_base_agent,
        synthesis_agent
    ):
        self.client = anthropic_client
        self.time_series_agent = time_series_agent
        self.image_agent = image_agent
        self.knowledge_base = knowledge_base_agent
        self.synthesis_agent = synthesis_agent
    
    async def analyze(self, production_data: List[Dict], period: tuple) -> Dict:
        """
        Main orchestration workflow
        """
        messages = []
        
        print("[Orchestrator] Phase 1: Statistical analysis...")
        stats_result = await self.time_series_agent.analyze(production_data)
        messages.append({
            "agent": "time_series",
            "result": stats_result
        })
        
        # Check if images needed
        if stats_result.get("requires_images"):
            print("[Orchestrator] Phase 2: Visual inspection...")
            for img_request in stats_result.get("image_requests", []):
                image_result = await self.image_agent.analyze({
                    **img_request,
                    "context": {
                        "hypothesis": stats_result.get("hypothesis"),
                        "statistical_evidence": stats_result.get("findings")
                    }
                })
                messages.append({
                    "agent": "image_analysis",
                    "result": image_result
                })
        
        # Query knowledge base
        print("[Orchestrator] Phase 3: Historical context...")
        kb_result = await self.knowledge_base.query(
            stats_result.get("findings", [])
        )
        messages.append({
            "agent": "knowledge_base",
            "result": kb_result
        })
        
        # Generate final report
        print("[Orchestrator] Phase 4: Report synthesis...")
        report = await self.synthesis_agent.generate_report(messages, period)
        
        return report
```

### Phase 3: Knowledge Base & Synthesis (Weeks 5-6)

**Goal**: Implement historical context and report generation

#### Step 3.1: Knowledge Base Agent

```python
# agents/knowledge_base_agent.py
from typing import List, Dict
import pinecone
from openai import OpenAI

class KnowledgeBaseAgent:
    def __init__(self, pinecone_index, postgres_conn):
        self.vector_db = pinecone_index
        self.sql_db = postgres_conn
        self.openai = OpenAI()
    
    async def query(self, findings: List[Dict]) -> Dict:
        """Query historical incidents and maintenance logs"""
        
        # Create query from findings
        query_text = self._create_query(findings)
        
        # Search for similar incidents
        similar_incidents = self._search_similar_incidents(query_text)
        
        # Get maintenance logs
        maintenance_logs = self._get_maintenance_logs(findings)
        
        return {
            "similar_incidents": similar_incidents,
            "maintenance_logs": maintenance_logs,
            "root_cause_hypotheses": self._generate_hypotheses(
                similar_incidents,
                findings
            )
        }
    
    def _create_query(self, findings: List[Dict]) -> str:
        """Convert findings to search query"""
        parts = []
        for finding in findings:
            parts.append(finding.get("description", ""))
        return " ".join(parts)
    
    def _search_similar_incidents(self, query_text: str, top_k: int = 5):
        """Search vector database for similar incidents"""
        # Generate embedding
        response = self.openai.embeddings.create(
            model="text-embedding-3-small",
            input=query_text
        )
        embedding = response.data[0].embedding
        
        # Search
        results = self.vector_db.query(
            vector=embedding,
            top_k=top_k,
            include_metadata=True
        )
        
        return [match['metadata'] for match in results['matches']]
    
    def _get_maintenance_logs(self, findings: List[Dict]) -> List[Dict]:
        """Query SQL database for maintenance records"""
        # Extract relevant equipment/lines from findings
        lines = set()
        for finding in findings:
            if 'line_id' in finding:
                lines.add(finding['line_id'])
        
        # Query database
        with self.sql_db.cursor() as cur:
            cur.execute("""
                SELECT * FROM maintenance_logs
                WHERE line_id = ANY(%s)
                AND date > NOW() - INTERVAL '90 days'
                ORDER BY date DESC
            """, (list(lines),))
            
            return [dict(row) for row in cur.fetchall()]
    
    def _generate_hypotheses(self, incidents, findings):
        """Generate root cause hypotheses from historical data"""
        # Group incidents by root cause
        root_causes = {}
        for incident in incidents:
            cause = incident.get('root_cause', 'unknown')
            if cause not in root_causes:
                root_causes[cause] = []
            root_causes[cause].append(incident)
        
        # Create hypotheses
        hypotheses = []
        for cause, related_incidents in root_causes.items():
            hypotheses.append({
                "root_cause": cause,
                "confidence": len(related_incidents) / len(incidents),
                "supporting_incidents": len(related_incidents),
                "typical_resolution": related_incidents[0].get('resolution')
            })
        
        return sorted(hypotheses, key=lambda x: x['confidence'], reverse=True)
```

#### Step 3.2: Insight Synthesis Agent

```python
# agents/synthesis_agent.py
from anthropic import Anthropic
from typing import List, Dict
import json

class InsightSynthesisAgent:
    def __init__(self, anthropic_client: Anthropic):
        self.client = anthropic_client
        self.system_prompt = """You are a production quality expert who synthesizes
        technical findings into actionable insights for production managers.
        
        Create comprehensive reports that:
        - Consolidate findings from multiple agents
        - Prioritize issues by impact and urgency
        - Generate root cause hypotheses
        - Recommend specific actions with timelines
        - Include confidence scores
        
        Your reports should be clear, actionable, and evidence-based.
        """
    
    async def generate_report(self, messages: List[Dict], period: tuple) -> Dict:
        """Generate final comprehensive report"""
        
        # Consolidate all findings
        all_findings = json.dumps(messages, indent=2)
        
        prompt = f"""Based on analysis from multiple specialized agents, generate a
        comprehensive production quality report.

Period: {period[0]} to {period[1]}

Agent Findings:
{all_findings}

Create a structured report with:

1. Executive Summary (2-3 sentences, business impact focus)
2. Key Findings (prioritized by severity/impact)
3. Root Cause Analysis (hypothesis with confidence)
4. Recommended Actions:
   - Immediate (< 4 hours)
   - Short-term (this week)
   - Long-term (this month)
5. Business Impact Assessment (cost, risk, customer impact)
6. Confidence Scores

Format as structured JSON that can be rendered as markdown."""

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=8192,
            system=self.system_prompt,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Parse report
        report = self._parse_response(response.content[0].text)
        return report
    
    def _parse_response(self, text: str) -> Dict:
        """Parse synthesized report"""
        # Extract JSON or create structured dict
        import re
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except:
                pass
        
        # Fallback: return text
        return {
            "executive_summary": text[:500],
            "full_report": text
        }
```

### Phase 4: Integration & Testing (Weeks 7-8)

**Goal**: Integration, testing, and initial deployment

#### Step 4.1: Main System Integration

```python
# main.py
from datetime import datetime, timedelta
from agents.orchestrator import OrchestratorAgent
from agents.time_series_agent import TimeSeriesAnalysisAgent
from agents.image_analysis_agent import ImageAnalysisAgent
from agents.knowledge_base_agent import KnowledgeBaseAgent
from agents.synthesis_agent import InsightSynthesisAgent
from anthropic import Anthropic
import asyncio

class ProductionQualitySystem:
    def __init__(self, config):
        # Initialize LLM clients
        self.anthropic = Anthropic(api_key=config.anthropic_api_key)
        
        # Initialize storage
        self.image_store = ProductionImageStore(config)
        self.vector_db = pinecone.Index(config.pinecone_index)
        self.time_series_db = connect_timescale(config)
        
        # Initialize agents
        self.time_series_agent = TimeSeriesAnalysisAgent(self.anthropic)
        self.image_agent = ImageAnalysisAgent(self.anthropic, self.image_store)
        self.knowledge_base = KnowledgeBaseAgent(
            self.vector_db,
            self.time_series_db
        )
        self.synthesis_agent = InsightSynthesisAgent(self.anthropic)
        
        # Initialize orchestrator
        self.orchestrator = OrchestratorAgent(
            self.anthropic,
            self.time_series_agent,
            self.image_agent,
            self.knowledge_base,
            self.synthesis_agent
        )
    
    async def analyze_shift(self, shift_date: datetime, shift_name: str):
        """Analyze a completed shift"""
        print(f"\n{'='*80}")
        print(f"Analyzing {shift_name} shift for {shift_date.date()}")
        print(f"{'='*80}\n")
        
        # Fetch production data for shift
        production_data = self._fetch_shift_data(shift_date, shift_name)
        
        # Run analysis
        report = await self.orchestrator.analyze(
            production_data,
            period=(shift_date, shift_date + timedelta(hours=8))
        )
        
        # Store report
        self._store_report(report, shift_date, shift_name)
        
        # Send alerts if needed
        if report.get('severity') == 'high':
            self._send_alert(report)
        
        return report
    
    async def daily_analysis(self, date: datetime):
        """Run daily comprehensive analysis"""
        # Analyze all shifts
        shifts = ['morning', 'afternoon', 'night']
        reports = []
        
        for shift in shifts:
            report = await self.analyze_shift(date, shift)
            reports.append(report)
        
        # Generate daily summary
        daily_summary = await self._generate_daily_summary(reports)
        return daily_summary

# Run analysis
async def main():
    config = load_config()
    system = ProductionQualitySystem(config)
    
    # Analyze yesterday
    yesterday = datetime.now() - timedelta(days=1)
    report = await system.daily_analysis(yesterday)
    
    print("\n" + "="*80)
    print("DAILY ANALYSIS COMPLETE")
    print("="*80)
    print(report['executive_summary'])

if __name__ == "__main__":
    asyncio.run(main())
```

#### Step 4.2: Scheduled Execution

```python
# scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from main import ProductionQualitySystem, load_config
from datetime import datetime, timedelta
import asyncio

async def analyze_completed_shift():
    """Run analysis on most recently completed shift"""
    system = ProductionQualitySystem(load_config())
    
    # Determine which shift just completed
    hour = datetime.now().hour
    if 6 <= hour < 8:  # Night shift just ended
        shift = 'night'
    elif 14 <= hour < 16:  # Morning shift just ended
        shift = 'morning'
    elif 22 <= hour < 24:  # Afternoon shift just ended
        shift = 'afternoon'
    else:
        return  # Not a shift change
    
    # Run analysis
    report = await system.analyze_shift(datetime.now(), shift)
    
    print(f"Completed analysis for {shift} shift")
    print(f"Severity: {report.get('severity', 'normal')}")

def main():
    scheduler = AsyncIOScheduler()
    
    # Run analysis at end of each shift
    scheduler.add_job(analyze_completed_shift, 'cron', hour='7,15,23')
    
    # Run daily summary
    scheduler.add_job(
        lambda: asyncio.create_task(daily_summary()),
        'cron',
        hour=8,
        minute=0
    )
    
    scheduler.start()
    
    print("Production Quality Analysis System started")
    print("Monitoring shifts: 7AM, 3PM, 11PM")
    
    # Keep alive
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

if __name__ == "__main__":
    main()
```

---

## Cost Analysis

### LLM API Costs

**Per Shift Analysis:**
- Time Series Analysis: ~5,000 tokens → $0.015
- Image Analysis: ~15,000 tokens + 12 images → $0.15
- Knowledge Base: ~3,000 tokens → $0.009
- Synthesis: ~8,000 tokens → $0.024
- **Total per shift: ~$0.20**

**Monthly Costs (3 shifts/day, 30 days):**
- API costs: $0.20 × 3 × 30 = **$18/month**
- Storage (S3): ~$50/month
- Databases: ~$100/month (managed services)
- Compute: ~$200/month (cloud VMs)
- **Total: ~$370/month**

### ROI Calculation

**Conservative Estimate:**
- Defects prevented: 10 incidents/month
- Average cost per incident: $3,000
- **Savings: $30,000/month**
- **ROI: 8,000%**

---

## Monitoring & Maintenance

### System Monitoring

```python
# monitoring.py
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Dict

@dataclass
class AnalysisMetrics:
    """Track system performance metrics"""
    analysis_duration_seconds: float
    tokens_used: int
    images_analyzed: int
    cost_usd: float
    confidence_score: float
    findings_count: int
    timestamp: datetime

class SystemMonitor:
    def __init__(self):
        self.logger = logging.getLogger("production_quality_system")
        self.metrics = []
    
    def log_analysis(self, metrics: AnalysisMetrics):
        """Log analysis run metrics"""
        self.metrics.append(metrics)
        
        self.logger.info(f"""
        Analysis Complete:
        - Duration: {metrics.analysis_duration_seconds:.1f}s
        - Tokens: {metrics.tokens_used}
        - Cost: ${metrics.cost_usd:.3f}
        - Confidence: {metrics.confidence_score:.2f}
        - Findings: {metrics.findings_count}
        """)
        
        # Alert if analysis takes too long
        if metrics.analysis_duration_seconds > 300:  # 5 minutes
            self.logger.warning("Analysis took longer than expected")
        
        # Alert if costs are high
        if metrics.cost_usd > 1.0:
            self.logger.warning(f"High analysis cost: ${metrics.cost_usd}")
    
    def get_daily_stats(self) -> Dict:
        """Get daily performance statistics"""
        today_metrics = [
            m for m in self.metrics
            if m.timestamp.date() == datetime.now().date()
        ]
        
        if not today_metrics:
            return {}
        
        return {
            "total_analyses": len(today_metrics),
            "total_cost": sum(m.cost_usd for m in today_metrics),
            "avg_duration": sum(m.analysis_duration_seconds for m in today_metrics) / len(today_metrics),
            "total_findings": sum(m.findings_count for m in today_metrics),
            "avg_confidence": sum(m.confidence_score for m in today_metrics) / len(today_metrics)
        }
```

### Health Checks

```python
# health_check.py
from datetime import datetime, timedelta

class SystemHealthCheck:
    def __init__(self, system):
        self.system = system
    
    async def run_health_check(self) -> Dict[str, bool]:
        """Verify all components are healthy"""
        checks = {}
        
        # Check database connectivity
        checks['time_series_db'] = await self._check_db_connection(
            self.system.time_series_db
        )
        
        # Check image storage
        checks['image_storage'] = await self._check_image_storage(
            self.system.image_store
        )
        
        # Check LLM API
        checks['llm_api'] = await self._check_llm_api(
            self.system.anthropic
        )
        
        # Check vector database
        checks['vector_db'] = await self._check_vector_db(
            self.system.vector_db
        )
        
        # Overall health
        checks['overall'] = all(checks.values())
        
        return checks
    
    async def _check_db_connection(self, db) -> bool:
        """Test database connection"""
        try:
            # Simple query
            db.cursor().execute("SELECT 1")
            return True
        except:
            return False
    
    async def _check_image_storage(self, store) -> bool:
        """Test image storage access"""
        try:
            # Try to list objects
            store.s3.list_objects_v2(Bucket=store.bucket, MaxKeys=1)
            return True
        except:
            return False
    
    async def _check_llm_api(self, client) -> bool:
        """Test LLM API connectivity"""
        try:
            # Simple API call
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=10,
                messages=[{"role": "user", "content": "test"}]
            )
            return True
        except:
            return False
    
    async def _check_vector_db(self, index) -> bool:
        """Test vector database"""
        try:
            # Describe index
            stats = index.describe_index_stats()
            return True
        except:
            return False
```

---

## Deployment Checklist

### Pre-Deployment
- [ ] All databases set up and tested
- [ ] LLM API keys configured
- [ ] Image storage configured and accessible
- [ ] Data pipelines tested with real production data
- [ ] Agents tested individually
- [ ] End-to-end workflow tested
- [ ] Cost monitoring in place
- [ ] Alert system configured

### Deployment
- [ ] Deploy to production environment
- [ ] Run initial analysis on historical data (validation)
- [ ] Set up scheduled jobs
- [ ] Configure monitoring dashboards
- [ ] Train operators/managers on report interpretation
- [ ] Establish feedback loop process

### Post-Deployment
- [ ] Monitor first week closely
- [ ] Collect feedback from users
- [ ] Adjust confidence thresholds if needed
- [ ] Fine-tune alert sensitivity
- [ ] Document learnings
- [ ] Plan iterative improvements

---

## Next Steps

1. **Start with Phase 1**: Set up data infrastructure
2. **Pilot with one production line**: Test with limited scope
3. **Iterate based on feedback**: Refine agents and reports
4. **Scale to all lines**: Roll out system-wide
5. **Continuous improvement**: Add new capabilities based on needs

The key to success is starting small, validating with real data, and iterating based on actual production needs.
