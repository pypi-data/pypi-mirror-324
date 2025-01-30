# owl_ab_test

A Python package for A/B testing statistical analysis. This package provides tools for analyzing the results of A/B tests with support for both proportion-based and revenue-based metrics.

## Installation

```bash
pip install owl_ab_test
```

## Features

- Calculate statistics for A/B tests including:
  - Proportion-based metrics (e.g., conversion rates)
  - Revenue-based metrics (e.g., revenue per user)
- Process multiple metrics simultaneously
- Generate visualizations of confidence intervals using Plotly
- Handle control and multiple treatment groups
- Built-in error handling for invalid inputs

## Usage

### Basic Example - Proportion Metrics

```python
from owl_ab_test import calculate_proportion_stats, process_stats, plot_confidence_intervals
import pandas as pd

# Calculate statistics for a single proportion metric
stats = calculate_proportion_stats(
    success_count=150,    # Number of successes in treatment group
    total_count=1000,     # Total sample size in treatment group
    control_success=120,  # Number of successes in control group
    control_total=1000,   # Total sample size in control group
    confidence_level=0.95 # Optional confidence level (default: 0.95)
)

print(f"Lift: {stats['lift']:.2%}")
print(f"P-value: {stats['p_value']:.4f}")
print(f"95% CI: ({stats['ci_lower']:.2%}, {stats['ci_upper']:.2%})")
```

### Basic Example - Revenue Metrics

```python
from owl_ab_test import calculate_revenue_stats

# Calculate statistics for a revenue metric
stats = calculate_revenue_stats(
    treatment_value=25.50,  # Mean revenue in treatment group
    treatment_std=15.20,    # Standard deviation in treatment group
    treatment_n=1000,       # Sample size in treatment group
    control_value=20.00,    # Mean revenue in control group
    control_std=14.80,      # Standard deviation in control group
    control_n=1000,         # Sample size in control group
    confidence_level=0.95   # Optional confidence level (default: 0.95)
)

print(f"Lift: {stats['lift']:.2%}")
print(f"P-value: {stats['p_value']:.4f}")
print(f"95% CI: ({stats['ci_lower']:.2%}, {stats['ci_upper']:.2%})")
```

### Processing Multiple Metrics

```python
# Example DataFrame structure
data = {
    'variant': ['control', 'treatment_a', 'treatment_b'],
    'bucketed_visitors': [1000, 1000, 1000],
    'trial_starts': [120, 150, 140],
    'purchases': [60, 75, 70],
    'revenue': [1200.0, 1500.0, 1400.0],
    'revenue_std': [800.0, 850.0, 820.0],
    'user_count': [1000, 1000, 1000]
}
df = pd.DataFrame(data)

# Configure metrics to analyze
metrics_config = {
    'trial_conversion': {
        'type': 'proportion',
        'success_col': 'trial_starts',
        'total_col': 'bucketed_visitors'
    },
    'purchase_conversion': {
        'type': 'proportion',
        'success_col': 'purchases',
        'total_col': 'bucketed_visitors'
    },
    'revenue_per_user': {
        'type': 'revenue',
        'value_col': 'revenue',
        'std_col': 'revenue_std',
        'n_col': 'user_count'
    }
}

# Process all metrics
results = process_stats(df, metrics_config)
```

### Visualizing Results

```python
# Create a confidence interval plot
metric_mapping = {
    'trial_conversion': 'Trial Conversion Rate',
    'purchase_conversion': 'Purchase Conversion Rate',
    'revenue_per_user': 'Revenue per User'
}

fig = plot_confidence_intervals(
    results,
    metric_mapping=metric_mapping,
    width=900,
    height=400
)
fig.show()
```

## API Reference

### calculate_proportion_stats

```python
calculate_proportion_stats(success_count, total_count, control_success, control_total, confidence_level=0.95)
```

Calculates statistical metrics for proportion-based A/B tests.

Parameters:
- `success_count` (int): Number of successes in treatment group
- `total_count` (int): Total sample size in treatment group
- `control_success` (int): Number of successes in control group
- `control_total` (int): Total sample size in control group
- `confidence_level` (float, optional): Confidence level for intervals (default: 0.95)

Returns:
- dict with keys:
  - `lift`: Relative improvement over control
  - `statistic`: Z-test statistic
  - `p_value`: Two-sided p-value
  - `ci_lower`: Lower bound of confidence interval for relative lift
  - `ci_upper`: Upper bound of confidence interval for relative lift

### calculate_revenue_stats

```python
calculate_revenue_stats(treatment_value, treatment_std, treatment_n,
                      control_value, control_std, control_n,
                      confidence_level=0.95)
```

Calculates statistical metrics for revenue-based A/B tests.

Parameters:
- `treatment_value` (float): Mean value in treatment group
- `treatment_std` (float): Standard deviation in treatment group
- `treatment_n` (int): Sample size in treatment group
- `control_value` (float): Mean value in control group
- `control_std` (float): Standard deviation in control group
- `control_n` (int): Sample size in control group
- `confidence_level` (float, optional): Confidence level for intervals (default: 0.95)

Returns:
- dict with keys:
  - `lift`: Relative improvement over control
  - `statistic`: T-test statistic
  - `p_value`: Two-sided p-value
  - `ci_lower`: Lower bound of confidence interval for relative lift
  - `ci_upper`: Upper bound of confidence interval for relative lift

### process_stats

```python
process_stats(df, metrics_config)
```

Processes multiple metrics for A/B test analysis, supporting both proportion and revenue metrics.

Parameters:
- `df` (pandas.DataFrame): DataFrame containing experiment data
  - Required columns: 'variant' plus columns specified in metrics_config
- `metrics_config` (dict): Configuration for metrics to analyze
  - Keys: metric names
  - Values: dict with the following structure:
    For proportion metrics:
    ```python
    {
        'type': 'proportion',
        'success_col': 'column_name',
        'total_col': 'column_name'
    }
    ```
    For revenue metrics:
    ```python
    {
        'type': 'revenue',
        'value_col': 'column_name',
        'std_col': 'column_name',
        'n_col': 'column_name'
    }
    ```

Returns:
- pandas.DataFrame with columns:
  - `Metric`: Name of the metric
  - `Group`: Variant name
  - `Value`: Raw proportion or value
  - `Lift`: Relative lift vs control
  - `Statistic`: Test statistic (Z-test for proportions, T-test for revenue)
  - `P-Value`: Two-sided p-value
  - `CI_Lower`: Lower confidence interval
  - `CI_Upper`: Upper confidence interval

### plot_confidence_intervals

```python
plot_confidence_intervals(results, metric_mapping=None, width=900, height=400)
```

Creates a visualization of confidence intervals for experiment results.

Parameters:
- `results` (pandas.DataFrame): Results DataFrame from process_proportion_stats
- `metric_mapping` (dict, optional): Maps metric names to display names
- `width` (int, optional): Plot width in pixels (default: 900)
- `height` (int, optional): Plot height in pixels (default: 400)

Returns:
- plotly.graph_objects.Figure: Interactive confidence interval plot

## Requirements

- Python >=3.7
- numpy
- pandas
- scipy
- plotly

## Notes

- The package uses z-test statistics for proportion metrics and t-test statistics for revenue metrics
- Confidence intervals are calculated for relative lift over control
- The visualization uses Plotly for interactive plots
- Treatment groups are compared against the control group specified by 'variant' == 'control'

## License

MIT License

## Contributing

Contributions are welcome! Please reach out to anika.ranginani@gmail.com