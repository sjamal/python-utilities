# Python Utilities

Reusable Python helper functions and common utilities for data processing, file I/O, visualization, and configuration management. Designed for use as a support library across other Python projects.

## Purpose

Utility scripts provide:
- Custom data processing functions
- File I/O helpers
- Visualization utilities
- Common calculations
- Configuration management

## Common Utilities

### File I/O
```python
def save_dataframe(df, filename, file_format='csv'):
    """Save dataframe in specified format."""
    if file_format == 'csv':
        df.to_csv(filename, index=False)
    elif file_format == 'excel':
        df.to_excel(filename, index=False)
    elif file_format == 'json':
        df.to_json(filename)
```

### Data Processing
```python
def remove_outliers(series, std_threshold=3):
    """Remove outliers using standard deviation."""
    mean = series.mean()
    std = series.std()
    return series[(series > mean - std_threshold * std) & 
                  (series < mean + std_threshold * std)]
```

### Visualization Helper
```python
def set_plot_style(figsize=(12, 6), dpi=100):
    """Set consistent plotting style."""
    import matplotlib.pyplot as plt
    plt.rcParams['figure.figsize'] = figsize
    plt.rcParams['figure.dpi'] = dpi
    plt.rcParams['font.size'] = 10
```

## File Naming

Use descriptive names:
- `*_utils.py` for utility functions
- `*_helpers.py` for helper functions
- `config.py` for configuration

## Related Projects

- [python-sysadmin-tools](https://github.com/sjamal/python-sysadmin-tools) — Infrastructure auditing and VM sizing utilities
- [python-data-processing](https://github.com/sjamal/python-data-processing) — ETL and data transformation pipelines
- [python-machine-learning](https://github.com/sjamal/python-machine-learning) — Model training and evaluation scripts
- [python-utilities](https://github.com/sjamal/python-utilities) — Shared helper functions and utilities
- [python-visualization](https://github.com/sjamal/python-visualization) — Data visualization scripts
- [python-youtube-tools](https://github.com/sjamal/python-youtube-tools) — YouTube API data collection and analysis
- [r-data-analysis](https://github.com/sjamal/r-data-analysis) — R statistical analysis and visualization