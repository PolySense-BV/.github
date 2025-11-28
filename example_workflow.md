# Multi-Agent System - Complete Workflow Example

This document shows a detailed example of how the multi-agent system would analyze the production data from November 28, 2025, with actual agent conversations and reasoning.

## Input Data Summary

**Period**: November 28, 2025 (Full day)  
**Line**: Line 3  
**Total Units**: ~36,220  
**Average Defect Rate**: 0.85%  
**Anomaly**: Temperature spike at 14:00-16:00 with corresponding defect rate increase

---

## Agent Conversation Flow

### TURN 1: Initial Statistical Analysis

**System → Orchestrator Agent:**
```
Analyze production quality for Line 3, November 28, 2025
Attached: time_series_data.json (7 hourly data points)
```

**Orchestrator → Time Series Analysis Agent:**
```
Please analyze the attached production statistics for Line 3 on Nov 28, 2025.
Identify any anomalies, trends, or quality issues.
```

**Time Series Analysis Agent (Internal Reasoning):**
```
Analyzing data points...

Baseline calculation (morning shift):
- 06:00: defect_rate=0.0060, temp=85.0°C, size_std_dev=1.8mm
- 07:00: defect_rate=0.0069, temp=85.5°C, size_std_dev=1.9mm
- Morning avg defect rate: 0.0065

Anomaly detection:
- 14:00: defect_rate=0.0171 (163% above morning avg) ⚠️
- 14:00: temp=92.3°C (+7.3°C from baseline) ⚠️
- 14:00: size_std_dev=3.2mm (+68% from baseline) ⚠️

- 15:00: defect_rate=0.0184 (183% above morning avg) ⚠️⚠️
- 15:00: temp=91.8°C (+6.8°C from baseline) ⚠️
- 15:00: size_std_dev=3.5mm (+84% from baseline) ⚠️⚠️

Correlation analysis:
- Temperature vs defect_rate: r=0.94 (strong positive correlation)
- Temperature vs size_std_dev: r=0.91 (strong positive correlation)
- Size defects account for 65-68% of defects during anomaly period

Recovery pattern:
- 16:00: Defects decreasing, temp dropping
- 18:00: Back to baseline levels

Hypothesis: Temperature spike caused material behavior changes leading to 
dimensional instability.

Recommendation: Visual inspection needed to confirm defect morphology.
```

**Time Series Analysis Agent → Orchestrator:**
```json
{
  "sender": "time_series_agent",
  "message_type": "response",
  "content": {
    "summary": "Significant quality incident detected during afternoon shift",
    "findings": [
      {
        "type": "anomaly",
        "severity": "high",
        "description": "Defect rate increased 163-183% during 14:00-15:00 period",
        "quantification": {
          "baseline_defect_rate": 0.0065,
          "peak_defect_rate": 0.0184,
          "increase_percentage": 183,
          "duration_hours": 4,
          "estimated_units_affected": 340
        }
      },
      {
        "type": "correlation",
        "description": "Strong correlation between temperature spike and defect rate",
        "metrics": {
          "correlation_coefficient": 0.94,
          "temperature_increase": 7.3,
          "baseline_temp": 85.0,
          "peak_temp": 92.3
        }
      },
      {
        "type": "defect_pattern",
        "description": "Size-related defects increased 3x during anomaly period",
        "details": {
          "normal_size_defects_per_hour": 13,
          "anomaly_size_defects_per_hour": 58,
          "size_variance_increase": "84%"
        }
      }
    ],
    "business_impact": {
      "units_affected": 340,
      "estimated_scrap_cost_usd": 3400,
      "customer_impact": "none (caught at line inspection)",
      "productivity_impact": "8% cycle time increase during incident"
    },
    "confidence": 0.92
  },
  "requires_followup": true,
  "suggested_next_steps": [
    {
      "action": "request_images",
      "time_range": ["2025-11-28T14:00:00Z", "2025-11-28T15:00:00Z"],
      "line_id": "Line_3",
      "sampling": "every_5_minutes",
      "focus": "size_defects",
      "reason": "Need visual confirmation of defect morphology to validate temperature-induced deformation hypothesis"
    }
  ]
}
```

---

### TURN 2: Visual Inspection Request

**Orchestrator (Decision Logic):**
```
Time series agent found high-severity anomaly with strong hypothesis.
Visual evidence is needed to validate hypothesis.
Routing request to Image Analysis Agent...
```

**Orchestrator → Image Analysis Agent:**
```json
{
  "request_type": "targeted_inspection",
  "time_range": ["2025-11-28T14:00:00Z", "2025-11-28T15:00:00Z"],
  "line_id": "Line_3",
  "sampling_strategy": "every_5_minutes",
  "context": {
    "hypothesis": "Temperature spike caused material warping/deformation",
    "statistical_evidence": {
      "temperature_increase": "7.3°C",
      "size_variance_increase": "84%",
      "defect_rate_increase": "183%"
    },
    "focus_areas": ["dimensional_accuracy", "warping", "deformation"]
  }
}
```

**Image Analysis Agent (Internal Processing):**
```
Retrieving images from storage...
Found 12 images in time range (14:00-15:00, every 5 min)

Image 1 (14:00:15):
- 4 products visible
- 1 product showing slight dimensional deviation
- Shape appears slightly distorted on edges

Image 3 (14:10:15):
- 4 products visible  
- 2 products showing visible warping
- Edge deformation clearly visible
- Material appears softer/more pliable

Image 7 (14:30:15):
- 4 products visible
- 3 products showing significant warping
- Clear deformation pattern: edges curling, center sagging
- Material structure appears compromised

Image 12 (14:55:15):
- 4 products visible
- 2 products showing warping (reduced from peak)
- Deformation less severe than 14:30

Pattern analysis:
- Progressive degradation from 14:00 to 14:30
- Peak severity at 14:30-14:45
- Gradual recovery after 15:00
- Defect morphology consistent with heat-induced material softening

Hypothesis validation: ✓ CONFIRMED
Visual evidence strongly supports temperature-induced material deformation.
```

**Image Analysis Agent → Orchestrator:**
```json
{
  "sender": "image_analysis_agent",
  "message_type": "response",
  "content": {
    "images_analyzed": 12,
    "products_examined": 48,
    "defective_products": 18,
    "visual_defect_rate": 0.375,
    "findings": [
      {
        "defect_type": "warping_deformation",
        "prevalence": "high",
        "severity_progression": [
          {"time": "14:00", "severity": "mild"},
          {"time": "14:15", "severity": "moderate"},
          {"time": "14:30", "severity": "severe"},
          {"time": "14:45", "severity": "moderate"},
          {"time": "15:00", "severity": "mild"}
        ],
        "description": "Products show progressive warping with edges curling and center sagging. Material structure appears compromised during peak temperature period."
      },
      {
        "defect_type": "dimensional_deviation",
        "measurements": {
          "normal_size_range_mm": "244.0-246.0",
          "observed_range_mm": "243.2-248.5",
          "max_deviation": "+2.5mm from spec"
        }
      }
    ],
    "visual_patterns": [
      "Edge curling (consistent across affected products)",
      "Center sagging/depression",
      "Surface texture changes indicating material softening",
      "Asymmetric deformation (suggesting uneven heating)"
    ],
    "hypothesis_validation": {
      "original_hypothesis": "Temperature spike caused material warping",
      "visual_evidence_support": "strong",
      "confidence": 0.95,
      "additional_insights": "Asymmetric deformation pattern suggests localized heating issue, possibly from cooling system malfunction rather than uniform ambient temperature increase"
    }
  },
  "confidence": 0.95
}
```

---

### TURN 3: Historical Context Query

**Orchestrator (Decision Logic):**
```
Strong evidence of temperature-induced defects confirmed.
Need historical context to identify root cause and solution.
Querying knowledge base...
```

**Orchestrator → Knowledge Base Agent:**
```json
{
  "query_type": "similar_incidents",
  "parameters": {
    "incident_characteristics": {
      "symptom": "temperature_spike_with_size_defects",
      "line": "Line_3",
      "temperature_deviation": "+7°C",
      "primary_defect_type": "dimensional"
    },
    "lookback_period_days": 365,
    "include": ["root_causes", "resolutions", "maintenance_logs"]
  }
}
```

**Knowledge Base Agent (Internal Processing):**
```
Searching vector database for similar incidents...
Embedding query: "temperature spike line 3 size defects warping dimensional"

Top matches:
1. Incident_20250615_Line3 (similarity: 0.89)
   - Temperature spike to 94°C
   - Root cause: Cooling system filter clogged
   - Resolution time: 2 hours
   
2. Incident_20250303_Line2 (similarity: 0.76)
   - Temperature spike to 89°C  
   - Root cause: HVAC failure
   - Resolution time: 4 hours

Retrieving maintenance logs for Line_3...
- Last cooling system service: Nov 1, 2025 (27 days ago)
- Last extruder calibration: Nov 26, 2025 (2 days ago)
- Next scheduled maintenance: Dec 1, 2025 (3 days away)

Cross-referencing defect patterns...
Historical pattern match: 85% similarity to June 15 incident
Both incidents show:
- Gradual temperature rise
- Localized heating signature
- Size defects concentrated in specific pattern
- Recovery after 4 hours

Root cause probability:
- Cooling system filter/blockage: 75%
- HVAC malfunction: 15%
- Other: 10%
```

**Knowledge Base Agent → Orchestrator:**
```json
{
  "sender": "knowledge_base_agent",
  "message_type": "response",
  "content": {
    "similar_incidents": [
      {
        "date": "2025-06-15",
        "line": "Line_3",
        "similarity_score": 0.89,
        "incident_summary": {
          "symptoms": "Temperature spike to 94°C, defect rate 2.1%, size defects",
          "root_cause": "Cooling system filter clogged",
          "resolution": "Filter replacement + system flush",
          "time_to_resolve": "2 hours",
          "units_affected": 820,
          "cost_impact": "$8,200"
        },
        "preventive_actions_taken": "Increased filter inspection frequency to bi-weekly",
        "notes": "Similar progressive pattern and recovery time"
      },
      {
        "date": "2025-03-03",
        "line": "Line_2",
        "similarity_score": 0.76,
        "incident_summary": {
          "symptoms": "Temperature spike to 89°C, defect rate 1.2%",
          "root_cause": "HVAC failure combined with high ambient temperature",
          "resolution": "HVAC repair + temporary cooling enhancement",
          "time_to_resolve": "4 hours",
          "units_affected": 450,
          "cost_impact": "$4,500"
        }
      }
    ],
    "maintenance_history": {
      "last_cooling_service": {
        "date": "2025-11-01",
        "days_ago": 27,
        "status": "completed",
        "next_due": "2025-12-01",
        "notes": "All systems nominal at time of service"
      },
      "recent_work": {
        "date": "2025-11-26",
        "type": "extruder_calibration",
        "notes": "Minor adjustments made. Not cooling-related."
      }
    },
    "root_cause_analysis": {
      "most_likely": {
        "cause": "Cooling system filter blockage or coolant flow restriction",
        "confidence": 0.75,
        "reasoning": [
          "85% pattern match to June incident (same root cause)",
          "Same line (Line_3) with same cooling system",
          "27 days since last maintenance (approaching service interval)",
          "Localized heating pattern indicates cooling issue vs ambient",
          "Progressive onset and 4-hour recovery consistent with thermal mass behavior"
        ]
      },
      "alternative_hypotheses": [
        {
          "cause": "HVAC malfunction",
          "confidence": 0.15,
          "reasoning": "Less likely given localized pattern, but possible"
        },
        {
          "cause": "Coolant pump degradation",
          "confidence": 0.10,
          "reasoning": "Would show more gradual onset over days"
        }
      ]
    },
    "recommended_diagnostics": [
      "Inspect cooling system filters",
      "Check coolant flow rates",
      "Verify coolant levels",
      "Check for blockages in cooling lines",
      "Review HVAC logs for Nov 28, 14:00-16:00"
    ]
  },
  "confidence": 0.88
}
```

---

### TURN 4: Final Synthesis

**Orchestrator → Insight Synthesis Agent:**
```json
{
  "task": "generate_comprehensive_report",
  "period": {
    "start": "2025-11-28T00:00:00Z",
    "end": "2025-11-28T23:59:59Z"
  },
  "agent_findings": [
    {
      "source": "time_series_agent",
      "confidence": 0.92,
      "key_findings": "Temperature spike +7.3°C correlated with 183% defect rate increase, 340 units affected"
    },
    {
      "source": "image_analysis_agent", 
      "confidence": 0.95,
      "key_findings": "Visual confirmation of heat-induced warping/deformation, progressive severity pattern"
    },
    {
      "source": "knowledge_base_agent",
      "confidence": 0.88,
      "key_findings": "85% match to previous incident with cooling filter root cause, 75% confidence same issue"
    }
  ],
  "request": "Synthesize into actionable report for production management"
}
```

**Insight Synthesis Agent (Internal Processing):**
```
Consolidating findings from 3 agents...

Confidence score calculation:
- Statistical evidence: 92% confidence
- Visual evidence: 95% confidence  
- Historical context: 88% confidence
- Combined confidence: 92% (weighted average with correlation bonus)

Root cause determination:
- Primary hypothesis: Cooling system filter blockage
- Confidence: 75% (from KB agent)
- Supporting evidence: Statistical + visual + historical
- Overall confidence: 85% (KB confidence + evidence bonus)

Impact assessment:
- Immediate: 340 units scrapped, $3,400 cost
- Broader: No customer impact, 8% productivity loss during incident
- Risk: If not addressed, likely recurrence

Action prioritization:
1. IMMEDIATE: Verify and fix cooling system (prevent recurrence today)
2. SHORT-TERM: Preventive maintenance advancement
3. LONG-TERM: Enhanced monitoring and early warning

Audience considerations:
- Production manager needs: Actions, timeline, impact
- Maintenance team needs: Specific diagnostics, parts
- Quality team needs: Defect details, customer impact
- Executive needs: Cost, risk, prevention
```

**Insight Synthesis Agent → Orchestrator (Final Report):**
```markdown
# Production Quality Analysis Report
**Line 3 - November 28, 2025**

---

## Executive Summary

Line 3 experienced a **4-hour quality incident** on November 28 during afternoon shift (14:00-18:00) resulting in elevated defect rates. The incident was successfully contained with no customer impact, but requires immediate attention to prevent recurrence.

**Key Metrics:**
- Overall daily defect rate: 0.85% (within spec, below 30-day baseline of 1.05%)
- Incident defect rate: 1.71% peak (183% above baseline)
- Units affected: ~340 units (0.94% of daily production)
- Financial impact: $3,400 in scrap costs
- Customer impact: **None** (defects caught at line inspection)

**Status:** ⚠️ **Requires immediate action** - Root cause identified with high confidence

---

## Detailed Findings

### 1. Temperature-Induced Quality Incident ⚠️ HIGH PRIORITY

**What Happened:**
Between 14:00-16:00, Line 3 experienced a temperature spike from 85°C (normal) to 92.3°C, causing material deformation and dimensional defects.

**Statistical Evidence** (Confidence: 92%):
- Temperature increased by 7.3°C above baseline
- Defect rate increased 183% (0.65% → 1.84%)
- Size-related defects increased 3x (13/hr → 58/hr)
- Strong correlation (r=0.94) between temperature and defects
- 8% cycle time increase during incident

**Visual Evidence** (Confidence: 95%):
- Analyzed 12 images, 48 products during incident window
- Progressive warping and deformation visible
- Peak severity at 14:30-14:45
- Defect morphology: Edge curling, center sagging, material softening
- Asymmetric deformation pattern suggests **localized** heating (not ambient)

**Pattern Timeline:**
```
14:00 ──► Temperature begins rising, mild warping appears
14:30 ──► Peak temperature, severe deformation  
15:00 ──► Temperature declining, defects moderating
18:00 ──► Return to normal operations
```

### 2. Root Cause Analysis

**Primary Hypothesis:** Cooling System Filter Blockage/Flow Restriction

**Confidence:** 85% (High)

**Supporting Evidence:**
1. **Historical Pattern Match** (85% similarity)
   - Identical incident occurred June 15, 2025 on same line
   - Root cause confirmed: Clogged cooling filter
   - Resolution: Filter replacement (2 hours)
   
2. **Maintenance Timing**
   - Last cooling service: November 1 (27 days ago)
   - Approaching 30-day service interval
   - No recent cooling system work
   
3. **Defect Pattern Analysis**
   - Localized heating signature (asymmetric deformation)
   - Rules out ambient/HVAC issues (would be uniform)
   - Progressive onset consistent with gradual flow restriction
   - 4-hour recovery matches thermal mass cooldown
   
4. **Correlation Strength**
   - Near-perfect correlation (r=0.94) temperature vs defects
   - Indicates direct causal relationship

**Alternative Hypotheses:**
- HVAC malfunction (15% probability) - less likely given localized pattern
- Coolant pump degradation (5% probability) - would show gradual multi-day onset

---

## Business Impact Assessment

### Financial Impact
| Category | Amount | Details |
|----------|--------|---------|
| Scrap Cost | $3,400 | 340 units @ $10/unit |
| Productivity Loss | ~$500 | 8% cycle time reduction × 4 hours |
| **Total Direct Cost** | **$3,900** | One-time incident cost |
| Prevented Cost | $34,000+ | Would have been daily recurring if not addressed |

### Operational Impact
- ✅ No customer shipments affected (caught at line inspection)
- ✅ No safety incidents
- ⚠️ 8% productivity reduction during 4-hour window
- ✅ Self-resolved (temperature returned to normal)

### Risk Assessment
- **Recurrence Risk:** HIGH (75%) if not addressed
  - Same root cause likely still present
  - Could occur any shift
- **Escalation Risk:** MEDIUM
  - Could affect other production lines if HVAC-related
  - Could worsen if cooling completely fails

---

## Recommended Actions

### 🔴 IMMEDIATE (Within 4 hours - before next shift)

**Priority 1: Cooling System Inspection**
- [ ] Inspect cooling system filters for blockage
- [ ] Measure coolant flow rates (compare to spec)
- [ ] Check coolant levels and quality
- [ ] Inspect cooling lines for restrictions
- [ ] If filter blockage found → Replace filter + system flush (Est: 2 hours)

**Expected Outcome:** Prevent recurrence during tonight's shift  
**Confidence:** 85% this resolves the issue

**Priority 2: Verification Testing**
- [ ] Monitor first hour of next shift with enhanced temperature logging
- [ ] Verify temperature stability < 86°C
- [ ] Inspect first 100 units for any size defects

### 🟡 SHORT-TERM (This Week)

**Priority 3: Preventive Maintenance Advancement**
- [ ] Advance scheduled Dec 1 cooling maintenance to this week
- [ ] Perform comprehensive cooling system evaluation
- [ ] Replace any degraded components proactively
- [ ] Consider filter upgrade (higher capacity or finer filtration)

**Priority 4: Review Temperature Control Parameters**
- [ ] Audit temperature control setpoints for Line 3
- [ ] Verify temperature sensor calibration
- [ ] Review historical temperature data for gradual drift patterns

**Priority 5: Cross-Line Assessment**  
- [ ] Check cooling systems on Line 1 & Line 2
- [ ] Preventive filter checks on all lines
- [ ] Ensure no systemic cooling issues

### 🟢 LONG-TERM (Next 30 Days)

**Priority 6: Enhanced Monitoring & Early Warning**
- [ ] Implement real-time temperature alerts (threshold: +3°C deviation)
- [ ] Add predictive cooling system monitoring
- [ ] Install coolant flow meters with trend analysis
- [ ] Create automated alert to maintenance when temp deviation detected

**Priority 7: Maintenance Schedule Optimization**
- [ ] Reduce cooling system service interval from 30 days → 21 days
- [ ] Implement condition-based monitoring (not just time-based)
- [ ] Track filter degradation patterns

**Priority 8: Operator Training Enhancement**
- [ ] Train operators on temperature spike response protocol
- [ ] Create escalation procedure for sustained temperature deviations
- [ ] Add temperature monitoring to shift handover checklist

---

## Root Cause - Solution Mapping

```
ROOT CAUSE (85% confidence):
Cooling filter blockage/restriction
    ↓
MECHANISM:
Reduced coolant flow → inadequate heat removal
    ↓
EFFECT:
Process temperature rise (+7.3°C)
    ↓
CONSEQUENCE:
Material softening → dimensional instability
    ↓
RESULT:
Warping/deformation defects (+183% defect rate)
    ↓
SOLUTION:
Filter replacement + enhanced monitoring
```

---

## Quality Incident Classification

**Severity:** ⚠️ **Medium-High**
- Contained at line inspection (no customer impact)
- Significant cost impact ($3,900)
- High recurrence risk if not addressed

**Containment Status:** ✅ **Contained**
- Self-resolved after 4 hours
- No defective units shipped
- Root cause identified

**Required Reporting:**
- Internal quality incident report: **Required**
- Customer notification: **Not required**
- Regulatory notification: **Not required**

---

## Supporting Evidence & Analysis Chain

This report synthesizes findings from multiple analysis layers:

1. **Statistical Analysis** → Identified anomaly, quantified impact, detected correlation
2. **Visual Inspection** → Confirmed defect morphology, validated hypothesis
3. **Historical Context** → Matched to previous incident, identified root cause
4. **Synthesis** → Integrated evidence, assessed confidence, prioritized actions

**Overall Confidence Score: 92%**
- Statistical evidence: 92%
- Visual evidence: 95%
- Historical pattern match: 88%
- Root cause hypothesis: 85%

---

## Appendix: Detailed Data

### Temperature & Defect Rate Timeline
| Time  | Temp (°C) | Defect Rate | Size Defects | Deviation |
|-------|-----------|-------------|--------------|-----------|
| 06:00 | 85.0      | 0.60%       | 12          | Baseline  |
| 07:00 | 85.5      | 0.69%       | 14          | Normal    |
| 14:00 | 92.3      | 1.71%       | 58          | +7.3°C ⚠️ |
| 15:00 | 91.8      | 1.84%       | 65          | +6.8°C ⚠️ |
| 16:00 | 89.5      | 1.50%       | 48          | +4.5°C ⚠️ |
| 17:00 | 87.2      | 1.20%       | 35          | +2.2°C    |
| 18:00 | 85.8      | 0.74%       | 15          | Normal    |

### Historical Incident Comparison
| Metric | June 15, 2025 | Nov 28, 2025 |
|--------|---------------|--------------|
| Temperature spike | +9°C | +7.3°C |
| Peak defect rate | 2.1% | 1.84% |
| Duration | 4 hours | 4 hours |
| Units affected | 820 | 340 |
| Root cause | Cooling filter | Cooling filter (suspected) |
| Resolution time | 2 hours | TBD |

---

## Next Steps & Follow-Up

**Immediate Actions Owner:** Maintenance Team Lead  
**Target Completion:** Before 22:00 shift start (4 hours)

**Follow-up Required:**
1. Maintenance team to report findings from cooling inspection
2. Quality team to verify first hour of next shift
3. Production manager to review and approve preventive maintenance advancement
4. Engineering to design enhanced temperature monitoring system

**Success Criteria:**
- ✅ Temperature stable <86°C for 24 hours
- ✅ Defect rate returns to baseline (<0.70%)
- ✅ No size defect clusters
- ✅ No recurrence for 30 days

---

**Report Generated:** November 28, 2025, 19:30  
**Analysis Period:** November 28, 2025, 00:00-23:59  
**System:** Multi-Agent Production Quality Analysis  
**Confidence:** 92% (High)
```

---

## Summary of Agent Contributions

| Agent | Key Contribution | Confidence |
|-------|------------------|------------|
| **Time Series Agent** | Detected anomaly, quantified impact, identified correlation, requested visual evidence | 92% |
| **Image Analysis Agent** | Confirmed defect morphology, validated temperature hypothesis, identified localized heating | 95% |
| **Knowledge Base Agent** | Found similar incidents, identified likely root cause, recommended diagnostics | 88% |
| **Insight Synthesis Agent** | Consolidated evidence, prioritized actions, created comprehensive report | 92% |

**Multi-Agent Advantage:**
- Each agent specialized in their domain
- Iterative refinement (stats → images → history)
- Cross-validation of hypothesis
- Comprehensive evidence chain
- High confidence in recommendations (85%+)

---

## System Metrics

**Analysis Completed In:** ~3 minutes (wall time)
- Statistical analysis: 45 seconds
- Image retrieval & analysis: 90 seconds
- Knowledge base query: 30 seconds
- Report synthesis: 45 seconds

**Data Processed:**
- 7 time-series data points (hourly aggregations)
- 12 production images
- 365 days of historical incidents
- 90 days of maintenance logs

**Cost Estimate (LLM API calls):**
- Time Series Agent: ~5,000 tokens ($0.015)
- Image Analysis Agent: ~15,000 tokens + 12 images ($0.15)
- Knowledge Base Agent: ~3,000 tokens ($0.009)
- Synthesis Agent: ~8,000 tokens ($0.024)
- **Total:** ~$0.20 per daily analysis

**ROI:**
- Analysis cost: $0.20
- Issue detected & prevented: $3,900 direct + $34,000 prevented
- ROI: **170,000:1**
