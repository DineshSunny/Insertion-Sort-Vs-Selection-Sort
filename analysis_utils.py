# analysis_utils.py

from scipy.stats import ttest_ind

def run_t_test(data1, data2, label1="Set 1", label2="Set 2"):
    t_stat, p_value = ttest_ind(data1, data2)
    print(f"T-Test between {label1} and {label2}:")
    print(f"  T-Statistic: {t_stat:.4f}")
    print("  P-Value: {p_value:.4f}")

    if p_value < 0.05:
        print("  Result: Statistically significant difference (p < 0.05)")
    else:
        print("  Result: No statistically significant difference (p ≥ 0.05)")
