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

**Primary Metrics:**

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

### Data Source

- **Dataset:** Google Cluster 2019 — Cell G
- **BigQuery Model:** `analytics.mart_hardware_workload`
- **Total Records:** 987
- **Unique Machines:** 802

### Insight 5 — Low Resource-to-Capacity Ratios

**Dataset Overview:**

| Metric | Result |
|---|---:|
| Total records | 987 |
| Unique machines | 802 |
| Average CPU-to-capacity ratio | 2.22% |
| Average memory-to-capacity ratio | 2.87% |
| Missing ratio values | 0 |

**Resource Utilization Distribution**

| Ratio Range | CPU Records | Memory Records |
|---|---:|---:|
| Below 5% | 932 (94.4%) | 870 (88.1%) |
| 5% to below 10% | 40 (4.1%) | 66 (6.7%) |
| 10% or higher | 15 (1.5%) | 51 (5.2%) |

**Key Finding:** 94.4% of records have CPU-to-capacity ratios below 5%, while 88.1% have memory-to-capacity ratios below 5%.

**Calculation Method:**

The data pipeline calculates resource-to-capacity ratios as follows:

- CPU ratio = Average CPU Usage / CPU Capacity
- Memory ratio = Average Memory Usage / Memory Capacity

The calculations are performed in `pipelines/google/google_hardware_workload_join.py` before the data is loaded into BigQuery.

**Interpretation:** The sampled Google Cluster workload records show low CPU-to-capacity and memory-to-capacity ratios, indicating a potential opportunity to investigate resource allocation efficiency.

**Potential Recommendation:** Evaluate workload consolidation and resource allocation strategies after validating the ratio definitions and accounting for peak demand and operational constraints.

### Analysis Limitations

- Results describe sampled records, not the percentage of unique machines that are underutilized.
- Ratio definitions and normalization must be verified before interpreting them as actual hardware utilization.
- No direct energy savings can be calculated from these records.
- Google Cell G workload records must not be directly joined to Google Cell A power readings.

---

## 3. Cloud Cost Analysis

### Data Source

- **Dataset:** AWS EC2 Pricing
- **BigQuery Model:** `analytics.mart_cloud_cost`
- **Total Records:** 87
- **Distinct Instance Types:** 87
- **Instance Families:** 9

### Insight 6 — Cloud Cost Efficiency

**Dataset Overview:**

| Metric | Result |
|---|---:|
| Total records | 87 |
| Distinct instance types | 87 |
| Regions represented | 1 |
| Region | us-east-1 |
| Pricing types represented | 1 |
| Pricing type | OnDemand |
| Missing hourly prices | 0 |
| Invalid or missing vCPU capacity | 0 |
| Invalid or missing memory capacity | 0 |

**Cost Findings:**

- The `c6i` family has the lowest average hourly cost per vCPU among the nine families, at **$0.0425**.
- The `r6i` family has the lowest average hourly cost per GB of memory, at **$0.007875**.
- The `r6i` memory cost per GB is approximately **62.9% lower** than `c6i`, based on the returned family-level averages.
- The `c6i` average cost per vCPU is approximately **44.1% lower** than `r7a`.
- The results show a trade-off between compute cost and memory cost: `c6i` is the lowest-cost family per vCPU, while `r6i` is the lowest-cost family per GB of memory.

**Key Finding:** Different AWS EC2 instance families offer different price-to-resource advantages. The most cost-effective family depends on whether the workload prioritizes CPU or memory capacity.

**Interpretation:** `c6i` may be a cost-effective option for workloads prioritizing vCPU cost, while `r6i` may be worth evaluating for memory-intensive workloads.

**Potential Recommendation:** Compare cloud instance families using workload-specific resource requirements instead of selecting instances based only on their hourly price.

### Analysis Limitations

- These are price-to-resource comparisons, not measurements of real application performance or energy efficiency.
- The analysis covers one region and one pricing type in the returned dataset.
- Findings should not be generalized to other regions or pricing plans.
- The lowest unit cost does not necessarily imply the lowest total cost for a workload.
- Workload requirements and instance sizing must also be considered.

---

## 4. Power Consumption Trends

### Data Source

- **Dataset:** Google Data Center — Cell A, PDU10
- **BigQuery Model:** `analytics.mart_power_trends`
- **Total Power Readings:** 8,928
- **Hourly Periods:** 744
- **Unique Hour Buckets:** 744

**Primary Metrics:**

- `avg_measured_power_util`: Average normalized measured power utilization
- `avg_production_power_util`: Average normalized production power utilization
- `total_readings`: Number of readings per hourly period
- `bad_measurement_count`: Number of invalid measured-power readings
- `bad_production_count`: Number of invalid production-power readings

### Insight 7 — Power Utilization Overview

**Dataset Overview:**

| Metric | Result |
|---|---:|
| Total power readings | 8,928 |
| Hourly periods | 744 |
| Average hourly measured utilization | 0.7360 |
| Average hourly production utilization | 0.6017 |
| Maximum hourly measured utilization | 0.7824 |
| Maximum hourly production utilization | 0.6382 |
| Invalid measured-power readings | 0 |
| Invalid production-power readings | 22 |

**Key Finding:** The dataset contains 744 hourly periods, representing 31 days of hourly observations, with variation in normalized measured and production power utilization.

**Interpretation:** The dataset supports time-based analysis of normalized power utilization and can help identify periods of elevated utilization.

**Potential Recommendation:** Monitor power utilization trends using time-series visualizations and investigate unusually high or low readings.

**Important Note:** The reported averages are averages of hourly aggregated values, not necessarily weighted averages of all original readings.

### Insight 8 — Peak Power Utilization Periods

The five highest hourly periods by average measured power utilization were:

| Hour Bucket | Measured Utilization | Production Utilization | Readings |
|---|---:|---:|---:|
| 223 | 0.7824 | 0.6162 | 12 |
| 295 | 0.7805 | 0.6155 | 12 |
| 271 | 0.7758 | 0.6100 | 12 |
| 247 | 0.7758 | 0.6102 | 12 |
| 273 | 0.7758 | 0.6178 | 12 |

**Key Findings:**

- Highest hourly average measured power utilization: **0.7824**, at hour bucket 223.
- Overall average hourly measured power utilization: **0.7360**.
- The highest hourly average was approximately **6.3% higher** than the overall hourly average.
- All five highest hourly periods contained 12 readings and no flagged invalid readings.

**Interpretation:** Measured power utilization varies across hourly periods, with identifiable peaks that may be useful for investigating operational patterns.

**Potential Recommendation:** Monitor high-utilization periods and investigate whether recurring time-based patterns exist.

### Insight 9 — Daily Power Utilization Pattern

**Analysis Method:**

Hourly power utilization was grouped using `MOD(hour_bucket, 24)` to investigate potential patterns across a relative 24-hour cycle.

**Key Findings:**

| Metric | Result |
|---|---|
| Highest average measured utilization | 0.7544 |
| Relative hour with highest average | 11 |
| Lowest average measured utilization | 0.7141 |
| Relative hour with lowest average | 19 |
| Difference | 0.0403 normalized units |
| Relative difference | Approximately 5.64% |
| Observations per relative hour | 31 |

**Finding:** Average measured power utilization varies across the relative 24-hour cycle, with higher average values around relative hours 10–13.

**Daily Peak Consistency Analysis:**

The number of days in which each relative hour appeared among the top three measured power-utilization hours was:

| Relative Hour | Days in Top 3 | Percentage of 31 Days |
|---|---:|---:|
| 12 | 13 | 41.9% |
| 10 | 10 | 32.3% |
| 11 | 10 | 32.3% |
| 13 | 10 | 32.3% |
| 7 | 9 | 29.0% |

**Additional Finding:** Relative hour 12 appeared among the top three highest-utilization hours on 13 out of 31 days. Relative hours 10, 11, and 13 each appeared in the top three on 10 days.

**Interpretation:** The results suggest a recurring period of elevated measured power utilization within the relative 24-hour cycle, although peak hours are not identical every day.

**Potential Recommendation:** Include a 24-hour utilization trend chart in the dashboard and investigate whether workload scheduling or other operational factors explain the observed pattern.

**Limitations:**

- Relative hours are calculated from the dataset's starting point and do not necessarily correspond to actual clock hours.
- The observed pattern does not establish its underlying operational cause.
- Daily variations should be considered before making workload scheduling decisions.

### Insight 10 — Power Data Quality and Invalid Readings

**Key Findings:**

- Total power readings: **8,928**
- Invalid production readings: **22 (approximately 0.25%)**
- Invalid measured-power readings: **0**
- Affected hourly periods: **0, 1, and 2**

| Hour Bucket | Invalid Production Readings | Total Readings | Average Production Utilization |
|---|---:|---:|---:|
| 0 | 3 | 12 | 0.6088 |
| 1 | 12 | 12 | NULL |
| 2 | 7 | 12 | 0.6026 |

**Finding:** All 22 invalid production readings occurred within the first three hourly periods. Hour bucket 1 contained no valid production readings, resulting in a NULL hourly production average.

**Interpretation:** Excluding invalid production readings preserves the reliability of calculated averages. A NULL value is appropriate when no valid observations are available.

**Recommendation:** Display missing production averages as unavailable rather than zero, and include data-quality indicators in the dashboard.

**Limitations:** The concentration of invalid readings at the beginning of the dataset does not establish their underlying cause.

### Power Analysis Limitations

- Power values represent normalized utilization, not physical power consumption in watts or energy in kWh.
- Normalized values cannot be directly converted into financial savings.
- Measured and production utilization metrics should not be subtracted to estimate wasted energy without validating their definitions.
- Google Cell A power readings cannot be directly attributed to individual machines in Google Cell G.

---

## 5. Final Recommendations

Based on the current analysis, the following recommendations are proposed:

### Recommendation 1 — Performance-Aware Server Selection

Filter server configurations by the required performance threshold, then rank eligible configurations by reported overall energy efficiency.

**Supporting Insights:** 1, 2, 3, and 4.

### Recommendation 2 — Investigate Resource Allocation Efficiency

Review workload placement and resource allocation strategies for records showing low CPU-to-capacity and memory-to-capacity ratios.

**Supporting Insight:** 5.

**Note:** Actual underutilization and potential energy savings require further validation.

### Recommendation 3 — Workload-Aware Cloud Cost Comparison

Compare AWS EC2 instance families based on the workload's CPU and memory requirements rather than hourly price alone.

**Supporting Insight:** 6.

### Recommendation 4 — Monitor Recurring Power Utilization Peaks

Use time-series monitoring to identify recurring periods of elevated normalized power utilization and investigate possible operational causes.

**Supporting Insights:** 7, 8, and 9.

### Recommendation 5 — Maintain Data Quality Controls

Exclude invalid readings from calculations, preserve missing values when no valid observations exist, and display data-quality indicators in the dashboard.

**Supporting Insight:** 10.

---

## 6. Dashboard Implementation Suggestions

The following dashboard features are proposed based on the analytical findings:

| Dashboard Section | Suggested Visualization or Feature |
|---|---|
| Server Efficiency | Top configurations ranked by overall efficiency |
| Server Recommendation | Interactive minimum performance threshold |
| Hardware & Workload | CPU and memory resource-to-capacity distributions |
| Cloud Cost | Cost per vCPU and cost per GB by instance family |
| Power Trends | Hourly normalized utilization time series |
| Daily Power Patterns | Average utilization by relative hour |
| Data Quality | Invalid-reading counts and missing-value indicators |

**Dashboard Goal:** Support data-driven exploration of server energy efficiency, hardware resource allocation, cloud pricing, and power utilization patterns.

**Important:** These analyses use different datasets and measurement contexts. Their findings should be presented as complementary perspectives rather than as directly linked measurements of the same infrastructure.

---

## 7. Overall Conclusion

The analysis demonstrates that data-driven infrastructure decisions require balancing multiple factors, including performance requirements, reported energy efficiency, hardware resource allocation, and cloud pricing.

SPECpower benchmark results show that the highest-ranked energy-efficient server configuration can change when the required performance threshold increases.

Google Cluster workload data highlights low resource-to-capacity ratios in the sampled records, suggesting opportunities for further resource allocation investigation.

AWS EC2 pricing comparisons show that different instance families provide different cost advantages depending on whether CPU or memory capacity is prioritized.

Google Data Center power data reveals measurable variation across hourly periods, potential recurring utilization patterns, and the importance of handling invalid readings correctly.

**Final Conclusion:** The project provides an analytical foundation for exploring energy-efficient infrastructure decisions while preserving performance requirements and acknowledging the limitations of each dataset.
