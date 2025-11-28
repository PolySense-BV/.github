# Multi-Agent Production Quality System - Visual Diagrams

## System Architecture Overview

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                         PRODUCTION FLOOR                               ┃
┃  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐             ┃
┃  │  Line 1  │  │  Line 2  │  │  Line 3  │  │  Line N  │             ┃
┃  │          │  │          │  │          │  │          │             ┃
┃  │ Sensors  │  │ Sensors  │  │ Sensors  │  │ Sensors  │             ┃
┃  │ Cameras  │  │ Cameras  │  │ Cameras  │  │ Cameras  │             ┃
┃  │ PLCs     │  │ PLCs     │  │ PLCs     │  │ PLCs     │             ┃
┃  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘             ┃
┃       │             │             │             │                     ┃
┗━━━━━━━┿━━━━━━━━━━━━━┿━━━━━━━━━━━━━┿━━━━━━━━━━━━━┿━━━━━━━━━━━━━━━━━━━┛
        │             │             │             │
        └─────────────┴─────────────┴─────────────┘
                      │
              ┌───────▼───────┐
              │  DATA GATEWAY │
              │  • Normalize  │
              │  • Aggregate  │
              │  • Validate   │
              └───────┬───────┘
                      │
        ┌─────────────┼─────────────┐
        │                           │
        ▼                           ▼
┏━━━━━━━━━━━━━━━┓         ┏━━━━━━━━━━━━━━━┓
┃  DATA STORAGE ┃         ┃ IMAGE STORAGE ┃
┃               ┃         ┃               ┃
┃ ┌───────────┐ ┃         ┃ ┌───────────┐ ┃
┃ │TimescaleDB│ ┃         ┃ │  AWS S3   │ ┃
┃ │           │ ┃         ┃ │           │ ┃
┃ │ Metrics   │ ┃         ┃ │ Line imgs │ ┃
┃ │ Time-series│┃         ┃ │ Metadata  │ ┃
┃ └───────────┘ ┃         ┃ └───────────┘ ┃
┗━━━━━━━┯━━━━━━━┛         ┗━━━━━━━┯━━━━━━━┛
        │                         │
        └─────────────┬───────────┘
                      │
                      ▼
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                    MULTI-AGENT AI SYSTEM                               ┃
┃                                                                         ┃
┃                    ┌─────────────────────┐                            ┃
┃                    │  ORCHESTRATOR AGENT │                            ┃
┃                    │                     │                            ┃
┃                    │  • Workflow control │                            ┃
┃                    │  • Context mgmt     │                            ┃
┃                    │  • Agent routing    │                            ┃
┃                    └──────────┬──────────┘                            ┃
┃                               │                                        ┃
┃              ┌────────────────┼────────────────┐                      ┃
┃              │                │                │                      ┃
┃              ▼                ▼                ▼                      ┃
┃   ┌────────────────┐ ┌────────────────┐ ┌────────────────┐          ┃
┃   │  TIME SERIES   │ │ IMAGE ANALYSIS │ │ KNOWLEDGE BASE │          ┃
┃   │     AGENT      │ │     AGENT      │ │     AGENT      │          ┃
┃   │                │ │                │ │                │          ┃
┃   │ Claude 3.5     │ │ Claude 3.5     │ │ Pinecone +     │          ┃
┃   │                │ │ (Vision)       │ │ PostgreSQL     │          ┃
┃   │ • Anomaly      │ │ • Defect detect│ │ • Similar      │          ┃
┃   │   detection    │ │ • Classification│ │   incidents    │          ┃
┃   │ • Correlations │ │ • Pattern recog│ │ • Root causes  │          ┃
┃   │ • Statistics   │ │ • Validation   │ │ • Maintenance  │          ┃
┃   └────────┬───────┘ └────────┬───────┘ └────────┬───────┘          ┃
┃            │                  │                  │                   ┃
┃            └──────────────────┼──────────────────┘                   ┃
┃                               │                                       ┃
┃                               ▼                                       ┃
┃                    ┌──────────────────┐                              ┃
┃                    │ INSIGHT SYNTHESIS│                              ┃
┃                    │      AGENT       │                              ┃
┃                    │                  │                              ┃
┃                    │ • Consolidate    │                              ┃
┃                    │ • Prioritize     │                              ┃
┃                    │ • Generate report│                              ┃
┃                    └────────┬─────────┘                              ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┿━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                                │
                                ▼
                    ┌───────────────────────┐
                    │   OUTPUT & ALERTS     │
                    │                       │
                    │  • Dashboard          │
                    │  • Email reports      │
                    │  • Slack alerts       │
                    │  • API endpoints      │
                    └───────────────────────┘
```

## Agent Interaction Flow

```
USER REQUEST: "Analyze production quality for Line 3, Nov 28, 2025"
     │
     ▼
┌─────────────────────────────────────────────────────────────────────┐
│ ORCHESTRATOR: "Let me coordinate the analysis..."                   │
└────┬────────────────────────────────────────────────────────────────┘
     │
     │ 1. INITIATE STATISTICAL ANALYSIS
     ▼
┌─────────────────────────────────────────────────────────────────────┐
│ TIME SERIES AGENT: "Analyzing statistics..."                        │
│                                                                      │
│ Input:  7 hours of production data                                  │
│         - Defect rates, temperatures, cycle times                   │
│                                                                      │
│ Process: [Uses statistical tools]                                   │
│         - Calculate baseline (morning avg)                          │
│         - Detect anomalies (Z-score > 3.0)                          │
│         - Correlation analysis (temp vs defects)                    │
│                                                                      │
│ Output: "ANOMALY DETECTED!"                                         │
│         - Defect rate increased 183% at 14:00-15:00                │
│         - Strong correlation with temp spike (+7.3°C)               │
│         - Confidence: 92%                                           │
│         - REQUEST: "Need images from 14:00-15:00"                   │
└────┬────────────────────────────────────────────────────────────────┘
     │
     │ 2. ROUTE IMAGE REQUEST
     ▼
┌─────────────────────────────────────────────────────────────────────┐
│ ORCHESTRATOR: "Time series found anomaly. Requesting visuals..."    │
└────┬────────────────────────────────────────────────────────────────┘
     │
     │ 3. VISUAL INSPECTION
     ▼
┌─────────────────────────────────────────────────────────────────────┐
│ IMAGE ANALYSIS AGENT: "Examining images..."                         │
│                                                                      │
│ Input:  12 images from 14:00-15:00                                  │
│         Context: "Temperature spike hypothesis"                     │
│                                                                      │
│ Process: [Vision analysis]                                          │
│         - Review each image                                         │
│         - Identify defect patterns                                  │
│         - Track progression over time                               │
│                                                                      │
│ Output: "HYPOTHESIS CONFIRMED!"                                     │
│         - Visual warping/deformation visible                        │
│         - Progressive severity (peak at 14:30)                      │
│         - Pattern consistent with heat-induced softening            │
│         - Confidence: 95%                                           │
└────┬────────────────────────────────────────────────────────────────┘
     │
     │ 4. QUERY HISTORICAL CONTEXT
     ▼
┌─────────────────────────────────────────────────────────────────────┐
│ ORCHESTRATOR: "Visual evidence supports hypothesis.                 │
│                Need historical context..."                          │
└────┬────────────────────────────────────────────────────────────────┘
     │
     │ 5. SEARCH KNOWLEDGE BASE
     ▼
┌─────────────────────────────────────────────────────────────────────┐
│ KNOWLEDGE BASE AGENT: "Searching history..."                        │
│                                                                      │
│ Input:  Query: "Line 3 temperature spike size defects"              │
│                                                                      │
│ Process: [Vector similarity search]                                 │
│         - Generate embedding                                        │
│         - Search incident database                                  │
│         - Retrieve maintenance logs                                 │
│                                                                      │
│ Output: "SIMILAR INCIDENT FOUND!"                                   │
│         - June 15, 2025: Same pattern (85% similarity)              │
│         - Root cause: Cooling filter blockage                       │
│         - Resolution: Filter replacement (2 hours)                  │
│         - Confidence: 88%                                           │
└────┬────────────────────────────────────────────────────────────────┘
     │
     │ 6. SYNTHESIZE FINDINGS
     ▼
┌─────────────────────────────────────────────────────────────────────┐
│ ORCHESTRATOR: "All agents complete. Synthesizing report..."         │
└────┬────────────────────────────────────────────────────────────────┘
     │
     │ 7. GENERATE COMPREHENSIVE REPORT
     ▼
┌─────────────────────────────────────────────────────────────────────┐
│ INSIGHT SYNTHESIS AGENT: "Creating actionable report..."            │
│                                                                      │
│ Input:  All agent findings                                          │
│         - Statistical: 92% confidence anomaly                       │
│         - Visual: 95% confidence defect pattern                     │
│         - Historical: 88% confidence root cause                     │
│                                                                      │
│ Process: [Synthesize & prioritize]                                  │
│         - Consolidate evidence                                      │
│         - Calculate overall confidence                              │
│         - Prioritize by impact                                      │
│         - Generate action items                                     │
│                                                                      │
│ Output: COMPREHENSIVE REPORT                                        │
│         ┌─────────────────────────────────────────┐                │
│         │ Executive Summary:                       │                │
│         │ Cooling filter blockage (85% confidence)│                │
│         │ 340 units affected, $3,400 cost         │                │
│         │                                          │                │
│         │ Immediate Action:                        │                │
│         │ [🔴] Inspect cooling filter NOW          │                │
│         │ [🟡] Advance scheduled maintenance       │                │
│         │ [🟢] Implement predictive alerts         │                │
│         └─────────────────────────────────────────┘                │
└────┬────────────────────────────────────────────────────────────────┘
     │
     │ 8. DELIVER RESULTS
     ▼
┌─────────────────────────────────────────────────────────────────────┐
│ ORCHESTRATOR: "Analysis complete. Report ready."                    │
└────┬────────────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────────────────┐
│ OUTPUT CHANNELS                                                      │
│  • Dashboard: Report published                                      │
│  • Email: Sent to production manager                                │
│  • Slack: Alert posted to #quality-alerts                           │
│  • API: Available via REST endpoint                                 │
└─────────────────────────────────────────────────────────────────────┘

Total Time: ~3 minutes
Total Cost: ~$0.20
Confidence: 85%
Business Impact: $3,400 prevented (+ $30,000+ future prevention)
```

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                    REAL-TIME DATA INGESTION                          │
└───┬─────────────────────────────────────────────────────────────┬───┘
    │                                                             │
    │ Every 1 minute                                    Every 5 minutes
    │                                                             │
    ▼                                                             ▼
┌────────────────────┐                                 ┌────────────────┐
│ Time-Series Metrics│                                 │     Images     │
│                    │                                 │                │
│ • Defect count     │                                 │ • Camera 1     │
│ • Temperature      │                                 │ • Camera 2     │
│ • Pressure         │                                 │ • Camera 3     │
│ • Cycle time       │                                 │ • Camera N     │
│ • Unit count       │                                 │ + Metadata     │
└────────┬───────────┘                                 └────────┬───────┘
         │                                                      │
         │ Store                                          Store │
         ▼                                                      ▼
┌────────────────────┐                              ┌──────────────────┐
│   TimescaleDB      │                              │     S3 Bucket    │
│                    │                              │                  │
│ Hypertable:        │                              │ Structure:       │
│ production_metrics │                              │ /YYYY/MM/DD/HH/  │
│                    │                              │   img_{ts}.jpg   │
│ Indexed by:        │                              │                  │
│ - time DESC        │                              │ Metadata:        │
│ - line_id          │                              │ - timestamp      │
│ - metric_name      │                              │ - line_id        │
│                    │                              │ - camera_id      │
│ Retention: 90 days │                              │ Retention: 30d   │
└────────┬───────────┘                              └──────────┬───────┘
         │                                                     │
         │                                                     │
         │                                                     │
         │      ┌──────────────────────────────┐              │
         └──────►   SCHEDULED ANALYSIS          │◄─────────────┘
                │                               │
                │ Triggers:                     │
                │ • End of shift (3x daily)     │
                │ • On-demand query             │
                │ • Continuous monitoring       │
                └───────────┬───────────────────┘
                            │
                            ▼
                ┌──────────────────────────────┐
                │   MULTI-AGENT ANALYSIS       │
                │                              │
                │ 1. Fetch data from DB        │
                │ 2. Run agent workflow        │
                │ 3. Generate insights         │
                └───────────┬──────────────────┘
                            │
                            ▼
                ┌──────────────────────────────┐
                │    HISTORICAL STORAGE        │
                │                              │
                │ • Vector DB (embeddings)     │
                │ • Reports archive            │
                │ • Incident database          │
                │                              │
                │ Used for:                    │
                │ - Future pattern matching    │
                │ - Root cause identification  │
                │ - System learning            │
                └──────────────────────────────┘
```

## Agent Decision Tree

```
                    ┌─────────────────┐
                    │ ORCHESTRATOR    │
                    │ receives request│
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Fetch production│
                    │      data       │
                    └────────┬────────┘
                             │
                    ┌────────▼─────────┐
                    │ TIME SERIES AGENT│
                    │  analyze stats   │
                    └────────┬─────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
         ┌──────▼──────┐          ┌──────▼──────┐
         │ Anomaly     │          │  No issues  │
         │ detected?   │          │  found      │
         └──────┬──────┘          └──────┬──────┘
                │ YES                    │ NO
                │                        │
         ┌──────▼──────┐                │
         │ Severity?   │                │
         └──────┬──────┘                │
                │                        │
      ┌─────────┴─────────┐             │
      │                   │             │
┌─────▼──────┐     ┌──────▼─────┐       │
│ HIGH/MED   │     │    LOW     │       │
│ severity   │     │  severity  │       │
└─────┬──────┘     └──────┬─────┘       │
      │                   │             │
      │ Request images    │ Skip images │
      │                   │             │
┌─────▼─────────────┐     │             │
│ IMAGE AGENT       │     │             │
│ analyze visuals   │     │             │
└─────┬─────────────┘     │             │
      │                   │             │
      │ ┌─────────────────┘             │
      │ │                               │
      └─┴───────────────────────────────┘
                      │
             ┌────────▼─────────┐
             │ KNOWLEDGE BASE   │
             │ query history    │
             └────────┬─────────┘
                      │
        ┌─────────────┴─────────────┐
        │                           │
  ┌─────▼──────┐            ┌───────▼─────┐
  │ Similar    │            │ No matches  │
  │ incidents  │            │ found       │
  │ found      │            │             │
  └─────┬──────┘            └───────┬─────┘
        │                           │
        │ High confidence           │ Lower confidence
        │ root cause                │ hypothesis
        └───────────┬───────────────┘
                    │
           ┌────────▼─────────┐
           │ SYNTHESIS AGENT  │
           │ generate report  │
           └────────┬─────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
  ┌─────▼──────┐        ┌───────▼──────┐
  │ High       │        │ Medium/Low   │
  │ severity   │        │ severity     │
  │ incident   │        │ finding      │
  └─────┬──────┘        └───────┬──────┘
        │                       │
        │ Immediate alert       │ Standard report
        │ + detailed report     │
        └───────────┬───────────┘
                    │
           ┌────────▼────────┐
           │ DELIVER RESULTS │
           │ - Dashboard     │
           │ - Email         │
           │ - Slack         │
           │ - API           │
           └─────────────────┘
```

## Confidence Score Calculation

```
┌──────────────────────────────────────────────────────────────────┐
│              OVERALL CONFIDENCE CALCULATION                       │
└──────────────────────────────────────────────────────────────────┘

Individual Agent Confidences:
├─ Time Series Agent:     92%  (strong statistical evidence)
├─ Image Analysis Agent:  95%  (clear visual confirmation)
└─ Knowledge Base Agent:  88%  (high similarity match)

                        │
        ┌───────────────┴───────────────┐
        │                               │
        ▼                               ▼
┌─────────────────┐           ┌──────────────────┐
│ BASE CONFIDENCE │           │ EVIDENCE BONUSES │
│                 │           │                  │
│ Weighted Avg:   │           │ • Cross-agent    │
│                 │           │   agreement: +3% │
│ (0.92 × 0.3) +  │           │                  │
│ (0.95 × 0.4) +  │     +     │ • Historical     │
│ (0.88 × 0.3)    │           │   match > 80%:+2%│
│                 │           │                  │
│ = 91.5%         │           │ • Visual         │
└────────┬────────┘           │   validation: +1%│
         │                    │                  │
         │                    │ Total: +6%       │
         │                    └──────────┬───────┘
         │                               │
         └───────────┬───────────────────┘
                     │
            ┌────────▼────────┐
            │ PENALTIES       │
            │                 │
            │ • Data gaps: 0% │
            │ • Contradictions│
            │   between agents│
            │   : 0%          │
            │                 │
            │ Total: -0%      │
            └────────┬────────┘
                     │
            ┌────────▼────────┐
            │ FINAL CONFIDENCE│
            │                 │
            │  91.5% + 6%     │
            │  = 97.5%        │
            │                 │
            │  Capped at 95%  │
            │  = 95%          │
            └─────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
┌──────────────┐          ┌──────────────┐
│ HIGH (>85%)  │          │ Display in   │
│              │          │ report:      │
│ "Very high   │          │              │
│  confidence  │          │ "95%         │
│  recommend   │          │  confidence" │
│  immediate   │          │              │
│  action"     │          │ + Evidence   │
│              │          │   breakdown  │
└──────────────┘          └──────────────┘
```

## Cost Optimization Strategy

```
┌─────────────────────────────────────────────────────────────────┐
│                    COST OPTIMIZATION FLOW                        │
└─────────────────────────────────────────────────────────────────┘

                    ┌─────────────────┐
                    │ ANALYSIS REQUEST│
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Quick Stats     │
                    │ Pre-Check       │
                    │                 │
                    │ • Basic calcs   │
                    │ • No LLM calls  │
                    │ • ~1 second     │
                    │ Cost: $0        │
                    └────────┬────────┘
                             │
                ┌────────────┴─────────────┐
                │                          │
         ┌──────▼──────┐           ┌───────▼──────┐
         │ All metrics │           │ Anomaly or   │
         │ normal      │           │ threshold    │
         │ (>80% days) │           │ exceeded     │
         └──────┬──────┘           └───────┬──────┘
                │                          │
         ┌──────▼──────┐                   │
         │ Generate    │                   │
         │ standard    │                   │
         │ report      │                   │
         │             │                   │
         │ No LLM call │                   │
         │ Cost: $0    │                   │
         └─────────────┘                   │
                                           │
                              ┌────────────▼────────────┐
                              │ TIME SERIES LLM AGENT   │
                              │                         │
                              │ • 5,000 tokens          │
                              │ • Cost: $0.015          │
                              └────────────┬────────────┘
                                           │
                              ┌────────────┴─────────────┐
                              │                          │
                       ┌──────▼──────┐           ┌───────▼──────┐
                       │ No visual   │           │ Requests     │
                       │ inspection  │           │ images       │
                       │ needed      │           │              │
                       │ (70% cases) │           │ (30% cases)  │
                       └──────┬──────┘           └───────┬──────┘
                              │                          │
                              │                          │
                              │              ┌───────────▼──────────┐
                              │              │ Sample images        │
                              │              │ intelligently:       │
                              │              │                      │
                              │              │ • Not all images     │
                              │              │ • Every 5 min sample │
                              │              │ • Max 12 images      │
                              │              │                      │
                              │              │ Reduces cost by 80%  │
                              │              └───────────┬──────────┘
                              │                          │
                              │              ┌───────────▼──────────┐
                              │              │ IMAGE ANALYSIS LLM   │
                              │              │                      │
                              │              │ • 15,000 tokens      │
                              │              │ • + 12 images        │
                              │              │ • Cost: $0.15        │
                              │              └───────────┬──────────┘
                              │                          │
                              └────────────┬─────────────┘
                                           │
                              ┌────────────▼────────────┐
                              │ KNOWLEDGE BASE          │
                              │                         │
                              │ • Vector search (cheap) │
                              │ • SQL query (cheap)     │
                              │ • 3,000 tokens          │
                              │ • Cost: $0.009          │
                              └────────────┬────────────┘
                                           │
                              ┌────────────▼────────────┐
                              │ SYNTHESIS LLM           │
                              │                         │
                              │ • 8,000 tokens          │
                              │ • Cost: $0.024          │
                              └────────────┬────────────┘
                                           │
                                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    TOTAL COST BREAKDOWN                          │
│                                                                  │
│  Scenario 1: Normal Day (80% of days)                           │
│  ├─ Pre-check: $0                                               │
│  ├─ Standard report: $0                                         │
│  └─ TOTAL: $0.00                                                │
│                                                                  │
│  Scenario 2: Minor Issue (15% of days)                          │
│  ├─ Time Series: $0.015                                         │
│  ├─ Knowledge Base: $0.009                                      │
│  ├─ Synthesis: $0.024                                           │
│  └─ TOTAL: $0.05                                                │
│                                                                  │
│  Scenario 3: Major Issue with Images (5% of days)               │
│  ├─ Time Series: $0.015                                         │
│  ├─ Image Analysis: $0.150                                      │
│  ├─ Knowledge Base: $0.009                                      │
│  ├─ Synthesis: $0.024                                           │
│  └─ TOTAL: $0.20                                                │
│                                                                  │
│  Monthly Average (3 shifts/day, 30 days):                       │
│  (0.80 × $0.00 × 90) + (0.15 × $0.05 × 90) + (0.05 × $0.20 ×90)│
│  = $0 + $0.68 + $0.90                                           │
│  = $1.58/month                                                  │
│                                                                  │
│  Worst case (every shift needs full analysis):                  │
│  $0.20 × 3 shifts × 30 days = $18/month                         │
└─────────────────────────────────────────────────────────────────┘
```

## Scalability Architecture

```
                         SINGLE LINE DEPLOYMENT
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  Line 1 → Data → Multi-Agent System → Reports                   │
│                                                                  │
│  Analysis time: 3 minutes                                       │
│  Cost per shift: $0.20                                          │
│  Concurrent capacity: 1 line                                    │
└─────────────────────────────────────────────────────────────────┘

                              ↓ Scale up ↓

                      MULTI-LINE DEPLOYMENT
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  Line 1 ─┐                                                      │
│  Line 2 ─┼→ Data Aggregator → Orchestrator ──┐                 │
│  Line 3 ─┤                                    │                 │
│  Line 4 ─┘                        ┌───────────┴─────────┐       │
│                                   │                     │       │
│                          ┌────────▼────────┐   ┌────────▼─────┐│
│                          │ Agent Pool 1    │   │ Agent Pool 2 ││
│                          │ (Lines 1-2)     │   │ (Lines 3-4)  ││
│                          └────────┬────────┘   └────────┬─────┘│
│                                   │                     │       │
│                                   └──────────┬──────────┘       │
│                                              │                  │
│                                    ┌─────────▼────────┐         │
│                                    │  Report Generator│         │
│                                    └──────────────────┘         │
│                                                                  │
│  Analysis time: 3-4 minutes (parallel processing)               │
│  Cost per shift: $0.60-0.80 (4 lines)                          │
│  Concurrent capacity: 4 lines                                   │
└─────────────────────────────────────────────────────────────────┘

                              ↓ Scale up ↓

                    ENTERPRISE DEPLOYMENT
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  Factory A (10 lines) ──┐                                       │
│  Factory B (12 lines) ──┼→ Central Data Lake                    │
│  Factory C (8 lines)  ──┘                                       │
│                              │                                   │
│                              ▼                                   │
│                  ┌──────────────────────┐                       │
│                  │ Orchestrator Cluster │                       │
│                  │ (Load Balanced)      │                       │
│                  └──────────┬───────────┘                       │
│                             │                                    │
│         ┌───────────────────┼───────────────────┐               │
│         │                   │                   │               │
│    ┌────▼────┐         ┌────▼────┐         ┌────▼────┐         │
│    │Agent    │         │Agent    │         │Agent    │         │
│    │Pool 1   │         │Pool 2   │         │Pool 3   │         │
│    │(10 inst)│         │(10 inst)│         │(10 inst)│         │
│    └────┬────┘         └────┬────┘         └────┬────┘         │
│         │                   │                   │               │
│         └───────────────────┼───────────────────┘               │
│                             │                                    │
│                             ▼                                    │
│                  ┌──────────────────────┐                       │
│                  │ Distributed Cache    │                       │
│                  │ (Redis)              │                       │
│                  └──────────────────────┘                       │
│                                                                  │
│  Analysis time: 3-5 minutes (highly parallel)                   │
│  Cost per shift: $5-10 (30 lines)                              │
│  Concurrent capacity: 30+ lines                                 │
│  High availability: Yes (redundancy)                            │
└─────────────────────────────────────────────────────────────────┘
```

---

These diagrams provide visual representations of:
1. Overall system architecture
2. Agent interaction and communication flow
3. Data ingestion and storage patterns
4. Decision-making logic
5. Confidence calculation methodology
6. Cost optimization strategies
7. Scalability options

Use these diagrams to:
- Explain the system to stakeholders
- Guide implementation decisions
- Understand data flows
- Optimize costs and performance
- Plan for scale
