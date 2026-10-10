# SPECpower Overall Efficiency Verification
# Source: Official SPECpower benchmark report

performance = [
    40017802, 36252933, 32246773, 28199831,
    24183842, 20153061, 16123742, 12092032,
    8050595, 4024453
]

power = [
    861, 812, 771, 710, 661,
    593, 515, 438, 367, 297
]

idle_power = 138
published_efficiency = 35920

total_performance = sum(performance)
total_power = sum(power) + idle_power

calculated_efficiency = total_performance / total_power

difference_pct = (
    abs(calculated_efficiency - published_efficiency)
    / published_efficiency
) * 100

print("Calculated Efficiency:", round(calculated_efficiency))
print("Published Efficiency:", published_efficiency)
print("Difference (%):", round(difference_pct, 4))
