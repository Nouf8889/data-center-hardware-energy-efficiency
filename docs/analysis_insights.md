# Data Center Hardware & Energy Efficiency
## Data Analysis — Insights & Findings

**Project Goal:** Identify energy-efficient server configurations that meet required performance levels without compromising performance.

**Data Platform:** Google BigQuery
**Transformation Tool:** dbt
**Analysis Status:** In Progress

---

## 1. Server Energy Efficiency Analysis

### Data Source
- **Dataset:** SPECpower Benchmark Data
- **BigQuery Model:** `analytics.mart_server_efficiency`
- **Valid Benchmark Records:** 1,116
- **Primary Metrics:**
  - `ssj_ops_100`: Performance at 100% load
  - `avg_watts_100`: Average power consumption at 100% load
  - `ssj_ops_per_watt`: Reported overall energy efficiency
  - `efficiency_100`: Energy efficiency at 100% load

### Insight 1 — Performance Eligibility

Using an illustrative minimum performance requirement of **5,000,000 ssj_ops**:

| Metric | Result |
|---|---:|
| Total valid records | 1,116 |
| Eligible records | 562 |
| Below requirement | 554 |
| Eligibility rate | 50.4% |

**Finding:** Approximately half of the benchmark records meet the selected minimum performance requirement.

**Interpretation:** Performance requirements should be applied before ranking configurations by energy efficiency.

### Insight 2 — Most Energy-Efficient Eligible Server

At a minimum performance requirement of 5 million ssj_ops, the highest-ranked benchmark record was:

| Attribute | Value |
|---|---|
| Server | Lenovo ThinkSystem SR665 V3 |
| CPU | AMD EPYC 9845 |
| CPU cores | 320 |
| RAM | 384 GB |
| Performance | 38,497,690 ssj_ops |
| Power at 100% load | 736 W |
| Overall energy efficiency | 44,648 ssj_ops/W |
| Efficiency at 100% load | 52,306.64 ssj_ops/W |

**Finding:** This configuration achieved the highest reported overall energy efficiency among the eligible benchmark records.

**Interpretation:** It is the leading candidate under the selected performance threshold and ranking metric.

### Insight 3 — Performance vs. Energy Efficiency Trade-off

The two highest-ranked eligible benchmark records were:

| Metric | Lenovo SR665 V3 | RS720A-E13-RS8U |
|---|---:|---:|
| CPU | AMD EPYC 9845 | AMD EPYC 9965 |
| Performance | 38.50M | 40.61M |
| Power at 100% load | 736 W | 800 W |
| Overall efficiency | 44,648 | 44,168 |

**Finding:** The Lenovo configuration achieved approximately **1.09% higher overall energy efficiency**, while the RS720A-E13-RS8U configuration delivered approximately **5.48% higher performance**.

**Interpretation:** Higher performance does not necessarily mean higher overall energy efficiency.

### Insight 4 — Performance-Aware Recommendations

Two illustrative performance scenarios were evaluated:

**Scenario A — Minimum Performance: 5 Million ssj_ops**

- Recommended configuration: Lenovo ThinkSystem SR665 V3
- CPU: AMD EPYC 9845
- Overall efficiency: 44,648 ssj_ops/W

**Scenario B — Minimum Performance: 40 Million ssj_ops**

- Recommended configuration: RS720A-E13-RS8U
- CPU: AMD EPYC 9965
- Overall efficiency: 44,168 ssj_ops/W

**Finding:** The highest-ranked eligible configuration changes when the required performance threshold increases.

**Recommendation:** Build a performance-aware recommendation feature that filters eligible server configurations before ranking them by energy efficiency.

### Analysis Limitations

- Performance thresholds are illustrative analytical scenarios, not actual customer service requirements.
- Benchmark records do not necessarily represent unique server configurations.
- Overall SPECpower efficiency and efficiency at 100% load are different metrics and should not be treated as interchangeable.
- Benchmark results may not reflect the performance or power consumption of a specific real-world workload.

---

## 2. Hardware & Workload Analysis

**BigQuery Model:** `analytics.mart_hardware_workload`

*Analysis pending.*

---

## 3. Cloud Cost Analysis

**BigQuery Model:** `analytics.mart_cloud_cost`

*Analysis pending.*

---

## 4. Power Consumption Trends

**BigQuery Model:** `analytics.mart_power_trends`

### Insight 5 — Low Resource-to-Capacity Ratios

**Data Source:** Google Cluster 2019 — Cell G
**BigQuery Model:** `analytics.mart_hardware_workload`

**Dataset Overview:**
- Total records: 987
- Unique machines: 802
- Average CPU-to-capacity ratio: 2.22%
- Average memory-to-capacity ratio: 2.87%
- Missing ratio values: 0

**Resource Utilization Distribution**

| Ratio Range | CPU Records | Memory Records |
|---|---:|---:|
| Below 5% | 932 (94.4%) | 870 (88.1%) |
| 5% to below 10% | 40 (4.1%) | 66 (6.7%) |
| 10% or higher | 15 (1.5%) | 51 (5.2%) |

**Key Finding:** 94.4% of records have CPU-to-capacity ratios below 5%, while 88.1% have memory-to-capacity ratios below 5%.

**Interpretation:** The sampled Google Cluster workload records show low CPU-to-capacity and memory-to-capacity ratios, indicating a potential opportunity to investigate resource allocation efficiency.

**Potential Recommendation:** Evaluate workload consolidation and resource allocation strategies after validating the ratio definitions and accounting for peak demand and operational constraints.

**Limitations:**
- Results describe sampled records, not the percentage of unique machines that are underutilized.
- Ratio definitions and normalization must be verified before interpreting them as actual hardware utilization.
- No direct energy savings can be calculated from these records.
- Google Cell G workload records must not be directly joined to Google Cell A power readings.
---



### 3. Cloud Cost Analysis

**Dataset:** `analytics.mart_cloud_cost`

#### Dataset Overview
- Total records: 87
- Distinct instance types: 87
- Regions represented: 1 (`us-east-1` in the returned pricing comparison)
- Pricing types represented: 1 (`OnDemand` in the returned pricing comparison)
- Hourly prices missing: 0
- Invalid or missing vCPU capacity: 0 records
- Invalid or missing memory capacity: 0 records

#### Cost Findings
- The `c6i` family has the lowest average hourly cost per vCPU among the nine families, at $0.0425.
- The `r6i` family has the lowest average hourly cost per GB of memory, at $0.007875.
- The `r6i` memory cost per GB is approximately 62.9% lower than `c6i`, based on the returned family-level averages.
- The `c6i` average cost per vCPU is approximately 44.1% lower than `r7a`.
- The results show a trade-off between compute cost and memory cost: `c6i` is the lowest-cost family per vCPU, while `r6i` is the lowest-cost family per GB of memory.

#### Interpretation and Limitations
- `c6i` may be a cost-effective option for workloads prioritizing vCPU cost, while `r6i` may be worth evaluating for memory-intensive workloads.
- These are price-to-resource comparisons, not measurements of real application performance or energy efficiency.
- The analysis covers one region and one pricing type in the returned dataset, so findings should not be generalized to other regions or pricing plans.
- The lowest unit cost does not necessarily imply the lowest total cost for a workload; workload requirements and instance sizing must also be considered.










## 5. Final Recommendations

*To be completed after all analytical models have been reviewed.*


