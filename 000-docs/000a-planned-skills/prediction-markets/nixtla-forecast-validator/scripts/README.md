# Nixtla Forecast Validator Scripts

Standalone Python scripts for validating time series forecast quality metrics.

## validate_forecast.py

Comprehensive validation script that compares current forecast metrics against historical benchmarks.

### Installation

```bash
pip install pandas matplotlib
```

### Usage

```bash
python validate_forecast.py \
  --historical historical_metrics.csv \
  --current current_metrics.csv \
  --mase_threshold 0.2 \
  --smape_threshold 0.2
```

### Arguments

- `--historical` (required): Path to historical metrics CSV file
- `--current` (required): Path to current metrics CSV file
- `--mase_threshold` (optional): Threshold for MASE deviation (default: 0.2)
- `--smape_threshold` (optional): Threshold for sMAPE deviation (default: 0.2)

### CSV Format

Input CSV files must contain these columns:
- `model`: Model identifier (string)
- `MASE`: Mean Absolute Scaled Error (float)
- `sMAPE`: Symmetric Mean Absolute Percentage Error (float)

### Output Files

- `validation_report.txt`: Summary of validation results
- `metrics_comparison.csv`: Side-by-side metric comparison
- `alert.log`: Alert messages for degraded models
- `metrics_visualization.png`: Bar chart visualization

### Example

```bash
# Create test data
cat > historical.csv << EOF
model,MASE,sMAPE
model_A,1.2,0.15
model_B,0.8,0.10
EOF

cat > current.csv << EOF
model,MASE,sMAPE
model_A,1.8,0.18
model_B,0.85,0.11
EOF

# Run validation
python validate_forecast.py --historical historical.csv --current current.csv

# Check results
cat validation_report.txt
```
